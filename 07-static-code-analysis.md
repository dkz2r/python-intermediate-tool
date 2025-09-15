---
title: 'Static Code Analysis'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- How do you write a lesson using R Markdown and `{sandpaper}`?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain how to use markdown with the new lesson template
- Demonstrate how to include pieces of code, figures, and nested challenge blocks

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

# These are Personal preference
# D203 - Don't require a space between the docstring and the class or function definition
# D212 - The summary of the docstring can go on the line below the triple quotes
ignore = ["D203", "D212"]
```

This configuration adds a number of additional rules to check for. This is the output from running
this one on our codebase:

```
I001 [*] Import block is un-sorted or un-formatted
 --> src\textanalysis_tool\readers\epub_reader.py:1:1
  |
1 | / import re
2 | |
3 | | from bs4 import BeautifulSoup
4 | | import ebooklib
5 | |
6 | | from textanalysis_tool.readers.base_reader import BaseReader
  | |____________________________________________________________^
  |
help: Organize imports

E501 Line too long (136 > 100)
  --> src\textanalysis_tool\readers\text_reader.py:10:101
   |
 8 | …
 9 | …)\]"
10 | …GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
   |                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 | …
12 | …
   |

I001 [*] Import block is un-sorted or un-formatted
 --> tests\readers\test_html_reader.py:1:1
  |
1 | / import pytest
2 | | from unittest.mock import mock_open
3 | |
4 | | from textanalysis_tool.readers.html_reader import HTMLReader
  | |____________________________________________________________^
5 |
6 |   TEST_DATA = """
  |
help: Organize imports

PLR2004 Magic value used in comparison, consider replacing `1234` with a constant variable
  --> tests\readers\test_html_reader.py:41:30
   |
39 |     assert metadata["title"] == "Test Document"
40 |     assert metadata["author"] == "Test Author"
41 |     assert metadata["id"] == 1234
   |                              ^^^^
   |

I001 [*] Import block is un-sorted or un-formatted
 --> tests\readers\test_text_reader.py:1:1
  |
1 | / import pytest
2 | | from unittest.mock import mock_open
3 | |
4 | | from textanalysis_tool.readers.text_reader import TextReader
  | |____________________________________________________________^
5 |
6 |   TEST_DATA = """
  |
help: Organize imports

PLR2004 Magic value used in comparison, consider replacing `1234` with a constant variable
  --> tests\readers\test_text_reader.py:40:30
   |
38 |     assert metadata["title"] == "Test Document"
39 |     assert metadata["author"] == "Test Author"
40 |     assert metadata["id"] == 1234
   |                              ^^^^
   |

PLR2004 Magic value used in comparison, consider replacing `1234` with a constant variable
  --> tests\test_document.py:21:50
   |
19 |     assert doc.title == "Test Document"
20 |     assert doc.author == "Test Author"
21 |     assert isinstance(doc.id, int) and doc.id == 1234
   |                                                  ^^^^
   |

PLR2004 Magic value used in comparison, consider replacing `2` with a constant variable
  --> tests\test_document.py:26:30
   |
24 | def test_line_count():
25 |     doc = Document(filepath="dummy_path.txt", reader=MockReader())
26 |     assert doc.line_count == 2
   |                              ^
   |

PLR2004 Magic value used in comparison, consider replacing `2` with a constant variable
  --> tests\test_document.py:31:47
   |
29 | def test_get_word_occurrence():
30 |     doc = Document(filepath="dummy_path.txt", reader=MockReader())
31 |     assert doc.get_word_occurrence("test") == 2
   |                                               ^
   |

Found 9 errors.
[*] 3 fixable with the `--fix` option.
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
uv run ruff check src/textanalysis_tool/document.py
```

It looks like we get six errors, all related to missing docstrings.

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
def get_word_occurrence(self, word: str) -> int:
    """
    Count the number of occurrences of the given word in the document content.

    Args:
        word (str): The word to count occurrences of.

    Returns:
        int: The number of occurrences of the word in the document content.

    """

    return self.content.lower().count(word.lower())
```

We can see that the Docstring is made up of different sections:

- A brief summary of what the function does
- An `Args` section that describes the function's parameters
- A `Returns` section that describes what the function returns

::: callout

Docstrings are not interpreted by python, so don't affect the runtime behavior of your code. They
are primarily for documentation purposes, and can be accessed using the built-in `help()` function.

:::

Running the `ruff` command again shows that we have fixed one of the issues in this file.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Docstrings for the Document Class

Add a docstring for the `document.py` module, the `Document` class, and the `__init__` method of the
`Document` class. Make sure to include a brief summary, as well as `Args` and `Returns` sections
where appropriate.

Refer to the [Google Style Guide - Comments in Modules](https://google.github.io/styleguide/pyguide.html#s3.8.2-comments-in-modules)
section for guidance.


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

Your output might look something like this:

```
src\textanalysis_tool\readers\html_reader.py:28: error: Item "None" of "PageElement | None" has no attribute "find_next_siblings"  [union-attr]
src\textanalysis_tool\readers\html_reader.py:40: error: Return type "str" of "get_metadata" incompatible with return type "dict[Any, Any]" in supertype "textanalysis_tool.readers.base_reader.BaseReader"  [override]
src\textanalysis_tool\readers\html_reader.py:43: error: Value of type "PageElement | None" is not indexable  [index]
src\textanalysis_tool\readers\html_reader.py:44: error: Value of type "PageElement | None" is not indexable  [index]
src\textanalysis_tool\readers\html_reader.py:45: error: Value of type "PageElement | None" is not indexable  [index]
src\textanalysis_tool\readers\html_reader.py:47: error: Item "None" of "Match[str] | None" has no attribute "group"  [union-attr]
src\textanalysis_tool\readers\html_reader.py:49: error: Incompatible return value type (got "dict[str, Any]", expected "str")  [return-value]
src\textanalysis_tool\readers\epub_reader.py:3: error: Skipping analyzing "ebooklib": module is installed, but missing library stubs or py.typed marker  [import-untyped]
src\textanalysis_tool\readers\epub_reader.py:3: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
src\textanalysis_tool\readers\epub_reader.py:31: error: Item "None" of "Match[str] | None" has no attribute "group"  [union-attr]
Found 9 errors in 2 files (checked 7 source files)
```

These errors are slightly more complex than the ones reported by `ruff`, but they are also very
useful, as the often point to places where our code might not handle all of the possible cases
correctly.

### Fixing Mypy Errors

MyPy Errors can be a bit tricky to understand, as they often involve a more complex analysis of the
code than `ruff`.

For example, the first error is telling us that we are trying to access the `find_next_siblings`
method on an object that could be `None`. This is a potential bug, as if the object is `None`,
this will raise an `AttributeError` at runtime.

Looking at the project code, the issue is in the `HTMLReader` class, in the `get_content` method:

```python
    def get_content(self, filepath) -> dict:
        soup = self.read(filepath)

        # Find the first h1 tag (The book title)
        title_h1 = soup.find("h1")

        # Collect all the content after the first h1
        content = []
        for element in title_h1.find_next_siblings():
            text = element.get_text(strip=True)

            # Stop early if we hit this text, which indicate the end of the book
            if "END OF THE PROJECT GUTENBERG EBOOK" in text:
                break

            if text:
                content.append(text)

        return "\n\n".join(content)
```

The `soup.find("h1")` call will return `None` if no `h1` tag is found in the HTML document. We
should probably add a check for this case and raise a more informative error message.

```python
    def get_content(self, filepath) -> dict:
        soup = self.read(filepath)

        # Find the first h1 tag (The book title)
        title_h1 = soup.find("h1")
        if title_h1 is None:
            raise ValueError(f"No <h1> tag found in the HTML document: {filepath}")

        # Collect all the content after the first h1
        content = []
        for element in title_h1.find_next_siblings():
            text = element.get_text(strip=True)

            # Stop early if we hit this text, which indicate the end of the book
            if "END OF THE PROJECT GUTENBERG EBOOK" in text:
                break

            if text:
                content.append(text)

        return "\n\n".join(content)
```

::: callout

Note that we don't have to actually change the code in the for loop, as `mypy` is smart enough to
understand that if `title_h1` is none, then the `ValueError` will be raised, and the code
following it will not be executed.

:::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Fix a Mypy Error

Another error we get is related to the `get_metadata` method in the same class:

```
src\textanalysis_tool\readers\html_reader.py:45: error: Value of type "PageElement | None" is not indexable  [index]
src\textanalysis_tool\readers\html_reader.py:46: error: Value of type "PageElement | None" is not indexable  [index]
src\textanalysis_tool\readers\html_reader.py:47: error: Value of type "PageElement | None" is not indexable  [index]
```

Why is this error being reported? What can we do to fix it? (There's actually two issues here! One
is a more specific `BeautifulSoup` issue, and the other is a more general Python issue.)

::: hint

Values in python dictionaries can be accessed in two ways:

- Using the indexing syntax: `value = my_dict[key]`
- Using the `get` method: `value = my_dict.get(key)`

The indexing syntax will raise a `KeyError` if the key is not found in the dictionary, while the
`get` method will return `None` (or a default value if provided) if the key is not found.

:::

::: hint

There are several kinds of values that can be returned from a `BeautifulSoup.find` call, and we
can't really be certain of which type we will get back. It could be a `Tag`, a `NavigableString`,
a `PageElement`, or `None`.

There is an alternative method called `select_one` that can be used to find elements using plain CSS
selectors, and it always returns either a `Tag` or `None`, which lets us avoid some of the
complexity of dealing with multiple possible types.

`soup.find("meta", {"name": "dc.title"})` can be replaced with
`soup.select_one('meta[name="dc.title"]')`

:::

:::::::::::::::: solution

MyPy is pointing out that we are using the indexing syntax to access values in a dictionary, but
given the way we are pulling the data out of the text, it is possible that the key might not even
be present in the dictionary.

We can fix this by using the `get` method instead, and providing a default value of `None` if the
key is not found.

```python
title_element = soup.select_one('meta[name="dc.title"]')
title = title_element.get("content") if title_element else "Unknown Title"

author_element = soup.select_one('meta[name="dc.creator"]')
author = author_element.get("content") if author_element else "Unknown Author"

url_element = soup.select_one('meta[name="dcterms.source"]')
url = url_element.get("content") if url_element else "Unknown URL"
```


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Fixing Other Mypy Errors

You should have at least one other mypy error in the `HTMLReader` class. Can you find it and fix
it? Do you have any other mypy errors in other parts of the codebase? If so, can you fix those as
well?

:::::::::::::::: solution

It will depend on your code!

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

::::::::::::::::::::::::::::::::::::::::::::::::

