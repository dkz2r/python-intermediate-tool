---
title: 'Creating A Module'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I create a Python module?
- How do I import a local module into my code?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Create a Python module with multiple files
- Import functions from a local module into a script

::::::::::::::::::::::::::::::::::::::::::::::::

## Project Organization

In order to keep our project organized, we'll start by creating some directories to put our code in.
So that we can keep the "source" code of our project separate from other aspects, we'll start by
creating a directory called "src". In this directory, we'll create a second directory with the name
of our module, in this case "vehicle-module". We can also delete the "main.py" file that was
generated automatically by uv. Your project folder should now look like this:

```
vehicle-module/
├── src/
│   └── vehicle_module/
├── .gitignore
├── .python-version
├── pyproject.toml
└── README.md
```

::: callout

Note that the interior folder has an underscore instead of a hyphen. We will import the module using
the name of the interior folder, `vehicle_module`. This is important as hyphens are not a valid
character in Python module names.

:::

Next, we'll create a file called `__init__.py` in the `src/vehicle_module` directory. This file
will make Python treat the directory as a package. Next to the `__init__.py` file, we can create
other Python files that will contain the code for our module.

::: callout

The `__init__.py` file is a special filename in python that indicated that the directory should be
treated as a package. Often these files are simply blank, however we can also include some
additional code to initialize the package or set up any necessary imports, as we will see later.

:::

Let's create a code file now, called `noises.py` and put a simple function in it:

```python

def honk_horn(times: int = 1):
    return "Honk! " * times

```

Our project folder should now look like this:

```
vehicle-module/
├── src/
│   └── vehicle_module/
│       ├── __init__.py
│       └── noises.py
├── .gitignore
├── .python-version
├── pyproject.toml
└── README.md
```

## Previewing Our Module

It's all well and good to write some code in here, but how can we actually use it? Let's create a
python script to test our module.

Let's create a directory called "tests", and start a new file called `test_noises.py` in it.

Add the following code to it:

```python
import vehicle_module

result = vehicle_module.noises.honk_horn(2)

if result == "Honk! Honk! ":
    print("Test passed!")
else:
    print("Test failed!")
```

::: callout

One of the really nice things about using `uv` is that we can replace `python` in our commands
with `uv run` and it will use the environment we have created for the project to run the code. At
the moment, this doesn't make a difference, but once we start adding dependencies to our project
we'll see how useful this is.

:::

Let's run the script from our command line. If you're in the root directory of the project, your
command will look something like `uv run tests/test_noises.py`.

Aaaand... It doesn't work!

```python
E:\Documents\Projects\vehicle-module>uv run tests/test_noises.py
Traceback (most recent call last):
  File "E:\Documents\Projects\vehicle-module\tests\test_noises.py", line 1, in <module>
    from vehicle_module.noises import honk_horn
ModuleNotFoundError: No module named 'vehicle_module'
```

The reason for this is that we never actually told python where it can find our code!

## The Python PATH

When you run a command like `import pandas`, what python actually does is search the a series of
directories in order looking for a module file called `pandas.py`. We can see what directories will
be checked by printing the `sys.path` variable.

```python
import sys
print(sys.path)
```

We are only interested in checking our current code, not in installing it as a package. However
because we have the `__init__.py` file in our package directory, if we add the exact or relative
path to our package directory to our `sys.path` variable, python will look there for modules as
well.

Let's add a quick line to the top of our testing script to add our specific module directory to
the path:

```python
import sys
sys.path.insert(0, "./src")

from vehicle_module.noises import honk_horn

result = hello("My Name")

if result == "Hello, My Name!":
    print("Test passed!")
else:
    print("Test failed!")
```

This time it works! And if we modify the `hello` function to print out something slightly
different, we can see that running the script changes the output right away!

::: callout

We used `sys.path.insert` instead of `sys.path.append` because we want to give our module directory
the highest priority when searching for modules. This way, if there are any naming conflicts with
other installed packages, our local module will be found first.

Ideally you would never be working with a package name that has a conflict elsewhere in the path
directories, but just in case, this avoids some potential issues.

:::

## Dot Notation in Imports

You probably noticed that our function call mimics the file and directory structure of the project.
We have the project directory (`vehicle_module`), then the filename (`noises`), and finally the function name (`honk_horn`). Python treats all of these similarly when trying to locate a function or module. We can also modify our import to make the code a little neater:

```python
import sys
sys.path.insert(0, "./src")

from vehicle_module import noises

result = noises.honk_horn(2)

if result == "Hello, My Name!":
    print("Test passed!")
else:
    print("Test failed!")
```

or even better:

```python
import sys
sys.path.insert(0, "./src")

from vehicle_module.noises import honk_horn

result = honk_horn(2)

if result == "Honk! Honk! ":
    print("Test passed!")
else:
    print("Test failed!")
```

::: callout

Fos simplicity here, we are using the `from ... import ...` syntax to import only the function we
need from the module. This way we don't have to include the module name every time we call the
function.

This is a common practice in python, however the absolute best practice would be to import the
entire module and then call the function with the module name, as in the first example. This way
we avoid potential naming conflicts with functions from other modules, as well as providing
clarity about where the function is coming from when reading the code.

:::

## The __init__.py File

We can see that in order to import our function, we have to include both the name of the module
and the name of the file before specifying the name of the function. Sometimes this can get
tedious, especially if there is a directory in our project with lots of files and different
functions in each file. This is where we can simplify things a little by adding a tiny bit of code
to our `__init__.py` file:

```python
from .noises import honk_horn
```

We can run our testing script just the same way as before and it will still work, but we can also
now leave out the `.noises` part:

```python
from vehicle_module import honk_horn

result = honk_horn(2)

if result == "Hello, My Name!":
    print("Test passed!")
else:
    print("Test failed!")
```

## Git Add / Commit

Before we forget, now that we have some simple code up and running, let's add it to our git
repository.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Add a Sub Module

Create a directory under `src/vehicle_module` called `greetings` and add a file called
`greet.py` with a function called greet that prints out the following:

```
Hello {User}!
It's nice to meet you!
```

How do you call this function from your testing script?

:::::::::::::::: solution

```python
from vehicle_module.engine.sounds import play_engine_sound

play_engine_sound(3000)
```

You could also include this line in our existing `__init__.py` file:

```python
from vehicle_module.engine.sounds import play_engine_sound
```

or add another `__init__.py` and include the following line:

```python
from vehicle_module.engine.sounds import play_engine_sound
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Inter-Module imports

Building on the last challenge, the first line of our greeting is identical to the output from our
`hello` function. How can we avoid code duplication by calling the `hello` function from within our
`greet` function?

:::::::::::::::: solution

In our greetings.py file:

```python
from vehicle_module import honk_horn

def play_engine_sound(rpm):
    return honk_horn(1) + f"\nVroom! Engine at {rpm} RPM"
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::: spoiler

Why are you bothering to write out the entire module path in greetings.py? Can't you just do this:

```python
from ..my_module import honk_horn

def play_engine_sound(rpm):
    honk_horn(1)
    print(f"Vroom! Engine at {rpm} RPM")
```

Yes, you absolutely can! The dot-notation used in python pathing can use `..` to refer to the
parent directory, or even `...` to refer to a grandparent directory.

The reason we're not doing this here is for clarity, as recommended in
[PEP8](https://www.python.org/dev/peps/pep-0008/#imports).

:::


::::::::::::::::::::::::::::::::::::: keypoints

- Python modules are simply directories with an `__init__.py` file in them
- You can add the path to your module directory to `sys.path` to make it available for import
- You can use dot notation in your imports to specify the module, file, and function you want to use

::::::::::::::::::::::::::::::::::::::::::::::::

