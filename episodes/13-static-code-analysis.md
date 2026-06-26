---
title: 'Static Code Analysis'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What is static code analysis?
- How can static code analysis tools help improve code quality?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Implement `ruff` and `mypy` in a Python project
- Understand how to read and fix issues reported by `ruff` and `mypy`

::::::::::::::::::::::::::::::::::::::::::::::::

## What is Static Code Analysis?

Static code analysis tools are programs or scripts that analyze source code without executing it
in order to identify potential issues, bugs, or code smells. These tools can help developers
improve code quality, maintainability, and adherence to coding standards.

We're going to look at two static code analysis tools in this episode: `ruff` and `mypy`.

Each of these tools can be run from the command line, and they can also be integrated into your
development workflow, such as in your text editor, as a pre-commit hook, or in your continuous
integration (CI) pipeline.

## Ruff

[Ruff](https://docs.astral.sh/ruff/) is a fast Python linter and code formatter that takes over
the roles of several other tools, including `flake8`, `pylint`, and `isort`.

We can install `ruff` as a development dependency using `uv`:

```bash
uv add ruff --dev
```

We can then run `ruff` on our codebase to identify any issues:

```bash
uv run ruff check .
```

Did you get any output? Depending on your IDE and it's settings, you might have already fixed some
of the issues.


The default configuration for `ruff` only checks for a few types of issues. We can customize the
configuration by adding a section for `ruff` in our `pyproject.toml` file:

```toml
[tool.ruff]
# Exclude specific files and directories from ruff
exclude = [
    ".venv",
    "__init__.py",
]
line-length = 100
indent-width = 4

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint]
# Enable specific linting rules
# - "D": Docstring-related rules (Not included for this workshop)
# - "E", "W": PEP8 style errors
# - "F": Flake8 compatibility
# - "I": Import-related rules (isort)
# - "B": Bugbear (Extended pycodesyle checks)
# - "PL": Pylint compatibility
# - "C90": McCabe complexity checks (identify code with large numbers of paths - should be refactored)
# - "N": Naming conventions for classes, functions, variables, etc.
# - "ERA": Remove commented out code
# - "RUF": Ruff-specific rules
# - "TID": Tidy Imports
select = ["E", "W", "F", "I", "B", "PL", "C90", "N", "ERA", "RUF", "TID", "SIM"]
```

This configuration adds a number of additional rules to check for. This is part of the output from
running `ruff` on our codebase:

```
I001 [*] Import block is un-sorted or un-formatted
 --> src\vehicle_module\car.py:1:1
  |
1 | / from datetime import datetime
2 | |
3 | | from .vehicle import Vehicle
4 | | from .engines.base_engine import BaseEngine
5 | | from .engines.gas_engine import GasEngine
  | |_________________________________________^
  |
help: Organize imports

F401 [*] `.engines.base_engine.BaseEngine` imported but unused
 --> src\vehicle_module\car.py:4:34
  |
3 | from .vehicle import Vehicle
4 | from .engines.base_engine import BaseEngine
  |                                  ^^^^^^^^^^
5 | from .engines.gas_engine import GasEngine
  |
help: Remove unused import: `.engines.base_engine.BaseEngine`

E501 Line too long (107 > 100)
  --> src\vehicle_module\car.py:27:101
   |
26 |     def __str__(self):
27 |         return f"A {self.color} {self.year} {self.make} {self.model} that runs on {self.engine.fuel_type}."
   |                                                                                                     ^^^^^^^
28 |
29 |     @property
   |

E501 Line too long (110 > 100)
  --> src\vehicle_module\car.py:44:101
   |
43 | class GasolineCar(Car):
44 |     pass  # For now, a GasolineCar is just a Car, so we don't need to add any additional properties or methods
   |                                                                                                     ^^^^^^^^^^
   |

PLR2004 Magic value used in comparison, consider replacing `10` with a constant variable
 --> src\vehicle_module\horn_noises.py:4:16
  |
2 |     if times < 1:
3 |         raise ValueError("Times must be at least 1")
4 |     if times > 10:
  |                ^^
5 |         raise ValueError("Times must be at most 10")
6 |     return ("Honk! " * times).strip()
  |

...

Found 12 errors.
[*] 6 fixable with the `--fix` option.
```

### Auto-fixing Issues

You notice right away that the end of the message says that 3 of the issues are fixable with the
`--fix` option. We can run `ruff` again with this option to automatically fix these issues:

```bash
uv run ruff check . --fix
```

Ruff will automatically fix issues that have very clear solutions, such as sorting imports and
fixing spacing. This command will modify your source files, so be sure to review the changes just
in case, but it should never modify the logic of your code.

### Ignoring Files and Rules

Some of the issues reported by `ruff` don't really make sense for our project. For example, it is
complaining about "magic numbers" in our tests. These are numbers that appear directly in the code
without being assigned to a named constant. In tests, this is often fine, since the numbers are
used in a clear context, and assigning them to a constant variable would just add unnecessary
complexity.

We can tell `ruff` to ignore specific rules for specific files or directories. We already have an
example of this in our `pyproject.toml` file, where we tell `ruff` to ignore the `__init__.py`
files in our codebase. We can add the following to ignore the magic number rule (`PLR2004`) in our
tests directory:

```toml
# Ignore magic number rule in tests
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004"]
```

## Docstrings

We we had removed the check for docstrings (`D`) from our `ruff` configuration, but let's just
re-enable it for a moment to see what it reports and how to fix it.

```bash
select = ["D", "E", "W", "F", "I", "B", "PL", "C90", "N", "ERA", "RUF", "TID", "SIM"]
```

To run `ruff` on a single file, we can specify the file path instead of a directory:

```bash
uv run ruff check src/vehicle_module/car.py
```

You should get several errors related to missing docstrings.

### What exactly is a docstring?

A docstring is a special type of comment that is used to document a module, class, method, or
function in Python. Docstrings are written using triple quotes (`"""`) and are placed immediately
after the definition of the module, class, method, or function they are documenting.

There are several different styles for writing docstrings:

- [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [NumPy Style](https://numpydoc.readthedocs.io/en/latest/format.html)
- [reStructuredText (reST) Style](https://peps.python.org/pep-0287/)

The choice of style often depends on the conventions used in a particular project or organization.

Let's stick with the Google style for this project. Here's an example of a docstring for one of the
functions in our `Document` class:

```python
    def paint(self, new_color):
        """
        Paint the car with a new color.

        Args:
            new_color (str): The new color for the car.

        Returns: None
        """
        self.color = new_color
```

We can see that the Docstring is made up of different sections:

- A brief summary of what the function does
- An `Args` section that describes the function's parameters
- A `Returns` section that describes what the function returns

::: callout

Docstrings are not interpreted by Python, so they don't affect the runtime behavior of your code.
They are primarily for documentation purposes, and can be accessed using the built-in `help()`
function.

:::

Running the `ruff` command again shows that we have fixed one of the issues in this file.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Docstrings for the Car Class

Add a docstring for the `car.py` file, the `Car` class, and the `__init__` method of the
`Car` class. Make sure to include a brief summary, as well as `Args` and `Returns` sections
where appropriate.

Refer to the [Google Style Guide - Comments in Modules](https://google.github.io/styleguide/pyguide.html#s3.8.2-comments-in-modules)
section for guidance.

See if you can get `ruff` to report no issues for this file.

:::::::::::::::: solution



:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

## Mypy

One of the common complaints about Python is that it is a dynamically typed language, which can
lead to type-related errors that are only caught at runtime. To help mitigate this, Python
supports type hints, which allow developers to specify the expected types of variables, function
parameters, and return values.

We've been using type hints all along in this project, but as these are only used by the IDE and
the user, there's no guarantee that the types are actually correct. This is where `mypy` comes in.

We can install `mypy` as a development dependency using `uv`:

```bash
uv add mypy --dev
```

Then run it on our codebase:

```bash
uv run mypy src
```

Nothing... Ok, I guess we were perfect! Except `mypy` doesn't check for type hints in files that
don't have any. Let's update our `pyproject.toml` file to tell `mypy` to check all files, even if
they don't have any type hints.

```toml
[tool.mypy]
# Check all files, even if they don't have any type hints
check_untyped_defs = true
```

Your output might look something like this:

```
src\vehicle_module\engines\hybrid_engine.py:8: error: Signature of "make_engine_noise" incompatible with supertype "vehicle_module.engines.base_engine.BaseEngine"  [override]
src\vehicle_module\engines\hybrid_engine.py:8: note:      Superclass:
src\vehicle_module\engines\hybrid_engine.py:8: note:          def make_engine_noise(self, rpm: Any) -> Any
src\vehicle_module\engines\hybrid_engine.py:8: note:      Subclass:
src\vehicle_module\engines\hybrid_engine.py:8: note:          def make_engine_noise(self) -> Any
src\vehicle_module\engines\gas_engine.py:8: error: Signature of "make_engine_noise" incompatible with supertype "vehicle_module.engines.base_engine.BaseEngine"  [override]
src\vehicle_module\engines\gas_engine.py:8: note:      Superclass:
src\vehicle_module\engines\gas_engine.py:8: note:          def make_engine_noise(self, rpm: Any) -> Any
src\vehicle_module\engines\gas_engine.py:8: note:      Subclass:
src\vehicle_module\engines\gas_engine.py:8: note:          def make_engine_noise(self) -> Any
src\vehicle_module\engines\electric_engine.py:8: error: Signature of "make_engine_noise" incompatible with supertype "vehicle_module.engines.base_engine.BaseEngine"  [override]
src\vehicle_module\engines\electric_engine.py:8: note:      Superclass:
src\vehicle_module\engines\electric_engine.py:8: note:          def make_engine_noise(self, rpm: Any) -> Any
src\vehicle_module\engines\electric_engine.py:8: note:      Subclass:
src\vehicle_module\engines\electric_engine.py:8: note:          def make_engine_noise(self) -> Any
src\vehicle_module\engines\diesel_engine.py:8: error: Signature of "make_engine_noise" incompatible with supertype "vehicle_module.engines.base_engine.BaseEngine"  [override]
src\vehicle_module\engines\diesel_engine.py:8: note:      Superclass:
src\vehicle_module\engines\diesel_engine.py:8: note:          def make_engine_noise(self, rpm: Any) -> Any
src\vehicle_module\engines\diesel_engine.py:8: note:      Subclass:
src\vehicle_module\engines\diesel_engine.py:8: note:          def make_engine_noise(self) -> Any
src\vehicle_module\car.py:10: error: Incompatible default for parameter "engine" (default has type "None", parameter has type "BaseEngine")  [assignment]
src\vehicle_module\car.py:10: note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no_implicit_optional=True
src\vehicle_module\car.py:10: note: Use https://github.com/hauntsaninja/no_implicit_optional to automatically upgrade your codebase
src\vehicle_module\car.py:34: error: Missing positional argument "rpm" in call to "make_engine_noise" of "BaseEngine"  [call-arg]
Found 6 errors in 5 files (checked 14 source files)
```

These errors are slightly more complex than the ones reported by `ruff`, but they are also very
useful, as the often point to places where our code might not handle all of the possible cases
correctly.

For example, what these errors point out is that in the BaseEngine class, the `make_engine_noise`
method takes an `rpm` argument, but in the subclasses, we have overridden this method without
including the `rpm` argument. This is a problem, as it means that the subclasses are not directly
compatible with the base class, and this could lead to unexpected behavior if we try to use a
subclass in place of the base class.

### Fixing Mypy Errors

MyPy Errors can be a bit tricky to understand, as they often involve a more complex analysis of the
code than `ruff`.

For this first issue, we can zero in on the `BaseEngine` class and the `make_engine_noise` method.
We can see that the method takes an `rpm` argument, but in the subclasses, don't ever use this
argument. We can fix this by removing the `rpm` argument from the base class method.

Re-running `mypy` should now show that this issue has been resolved.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Fix a Ruff Error


:::::::::::::::: solution


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Fix a MyPy Error

:::::::::::::::: solution


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

- There are many static code analysis tools available for Python, each with its own strengths and
  weaknesses.
- Ruff is a fast linter and code formatter that can replace several other tools, including
  `flake8`, `pylint`, and `isort`.
- MyPy is a static type checker that can help catch type-related errors in Python code.

::::::::::::::::::::::::::::::::::::::::::::::::

