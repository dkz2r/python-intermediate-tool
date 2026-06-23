---
title: 'Unit Testing'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What is unit testing?
- Why is unit testing important?
- How do you write a unit test in Python?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the concept of unit testing
- Demonstrate how to write and run unit tests in Python using `pytest`

::::::::::::::::::::::::::::::::::::::::::::::::

## Unit Testing

We have our little test files, but you might imagine that it's not particularly efficient to
always write individual scripts to test our code. What if we had a lot of functions or classes?
Or a lot of different ideas to test? What if our objects changed down the line? Our existing
modules are going to be difficult to maintain, and, as you may have expected, there is already a
solution for this problem.

### What Makes For a Good Test?

A good test is one that is:
- **Isolated**: A good test should be able to run independently of other tests, and should not rely
   on external resources such as databases or web services.
- **Repeatable**: A good test should produce the same results every time it is run.
- **Fast**: A good test should run quickly, so that it can be run frequently during development.
- **Clear**: A good test should be easy to understand, so that other developers can easily see what
   is being tested and why. Not just in the output provided by the test, but the variables,
   function names, and structure of the test should be clear and descriptive.

It can be easy to get carried away with testing everything and writing tests that cover every
single case that you can come up with. However having a massive test suite that is cumbersome to
update and takes a long time to run is not useful. A good rule of thumb is to focus on testing the
most important parts of your code, and the parts that are most likely to break. This often means
focusing on edge cases and error handling, rather than trying to test every possible input.

Generally, a good test module will test the basic functionality of an object or function, as well
as a few edge cases.

::: discussion

What are some edge cases that you can think of for the `honk_horn` function we wrote earlier?

What about the `calculate_liters_per_100km` function?

:::

::: spoiler

Some edge cases for the `honk_horn` function could include:

- The user provides a negative number for `times`
- The user provides a non-integer value for `times`
- The user provides a very large number for `times`

Some edge cases for the `calculate_liters_per_100km` function could include:

- Passing in a distance of zero
- Passing in a negative distance
- Passing in a negative amount of liters
- Passing in non-numeric values for either parameter

:::

## pytest

`pytest` is a testing framework for Python that helps to write simple and scalable test cases. It
is widely used in the python community, and has in-depth and comprehensive documentation. We won't
be getting into all of the different things you can do with pytest, but we will cover the basics
here.

To start off with, we need to add pytest to our environment. However unlike our previous packages,
`pytest` is not required for our module to work, it is only used by us as we are writing code.
Therefore it is a "development dependency". We can still add this to our `pyproject.toml` file via
uv, but we need to add a special flag to our command so that it goes in the correct place.

```bash
uv add pytest --dev
```

If you open up your `pyproject.toml` file, you should see that `pytest` has been added under a new
called "dependency groups" (your version number may be different):

```toml
[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```

Now we can start creating our tests.

### Writing a pytest Test File

Part of `pytest` is the concept of "test discovery". This means that pytest will automatically find
any test files that follow a certain naming convention. By default, pytest will look for files
that start with `test_` or end with `_test.py`. Inside these files, pytest will look for functions
that start with `test_`.

Our test file doesn't start with `test_`. There is a way to change the naming convention that
pytest uses, but for now, let's just rename our test file to `test_vehicle_module.py`.

Next, let's create a test for our `honk_horn` function based on the one we wrote before. Add a
function at the top of the file like this

```python
import sys

sys.path.insert(0, "./src")

import vehicle_module

def test_honk_horn():
    assert vehicle_module.horn_noises.honk_horn(2) == "Honk! Honk! "
```

`pytest` uses the `assert` statement to check if the output of a function is what we expect. If the
assertion is True, then the test passes. If the assertion is False, then the test fails. Tests can
have multiple assertions, and all of them need to be True for the test to pass.

In our previous test file, we had to add the path to our module each time. Now that we are using
`pytest`, we can use a special file called `conftest.py` to add this path automatically. Create a
file called `conftest.py` in the `tests` directory and add the following code to it:

```python
import sys

sys.path.insert(0, "./src")
```

Then we can remove the `sys.path.insert` line from our test file, and just have the import statement:

```python
import vehicle_module

def test_honk_horn():
    assert vehicle_module.honk_horn(2) == "Honk! Honk! "
```

::: instructor

This is how I always do it, but I assume there's a better way.

:::

Now, we just need to run the tests. We can do this with the following command:

```bash
uv run pytest
```

::: callout

Note that we are using `uv run` to run `pytest`, this ensures that `pytest` is run in the correct
environment with all the dependencies we have installed.

:::

You should see output similar to the following:

```
============================= test session starts ==============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: E:\Documents\Projects\vehicle-module
configfile: pyproject.toml
collected 1 item

tests\test_vehicle_module.py .                                            [100%]

============================== 1 passed in 0.03s ===============================
```

Why didn't it run the other test code? Because the need to be in functions that start with `test_`.
This is part of the test discovery process that pytest uses. If we want to test other functions, we
can add more functions.

Let's convert the rest of our tests to `pytest` tests. The updated test file should look like this:

```python
import vehicle_module


def test_honk_horn():
    assert vehicle_module.horn_noises.honk_horn(2) == "Honk! Honk! "


def test_play_engine_sound():
    assert (
        vehicle_module.engine_noise.play_engine_sound(3000) == "Honk! \nVroom! Engine at 3000 RPM"
    )


def test_calculate_liters_per_100km():
    assert vehicle_module.efficiency.fuel.calculate_liters_per_100km(km=50, liters=2.5) == 5.0
```

Let's run our tests again:

```bash
uv run pytest
```

You should see output similar to the following:

```
============================= test session starts ==============================
platform win32 -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: E:\Documents\Projects\vehicle-module
configfile: pyproject.toml
collected 4 items

tests\test_vehicle_module.py ...                                [100%]
============================== 3 passed in 0.15s ===============================
```

You can see that all of the tests have passed. There is a small green pip for each test that was
performed, and a summary at the end. Compare this to the test file we had before. We got rid of all
of the if statements, and just use the `assert` statement to check if the output is what we expect.

### Testing Exceptions

We usually want to test the most basic use case of our functions, but maybe we want to also check
for some common Edge Cases - situations that are not necessarily expected, but that we want to
anticipate and handle in our code. For example, what if the user provides a value of 0 for the
`times` parameter in the `honk_horn`. What should happen?

After our `test_honk_horn` function, add the following test:

```python
def test_honk_horn_zero():
    assert vehicle_module.horn_noises.honk_horn(0) == ""
```

Run the tests again:

```bash
uv run pytest
```

We get passing tests, which is what we expect. But we are the ones in charge of the function, what
if we say that if the user provides a value of 0 or less, we want the function to raise a
`ValueError`? We can write a test that checks not only for the output of the function, but also for
which exception it raises. Update the `test_honk_horn_zero` function to the following:

```python
import pytest

# Existing code

def test_honk_horn_zero():
    with pytest.raises(ValueError):
        vehicle_module.horn_noises.honk_horn(0)
```

Run the tests again:

```bash
uv run pytest
```

```
================================= FAILURES =====================================
_____________________________ test_honk_horn_zero ______________________________

    def test_honk_horn_zero():
>       with pytest.raises(ValueError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

tests\test_vehicle_module.py:11: Failed
============================= short test summary info ==========================
FAILED tests/test_vehicle_module.py::test_honk_horn_zero - Failed: DID NOT RAISE ValueError
========================== 1 failed, 3 passed in 0.13s =========================
```

This time, we get a failing test, because the `honk_horn` function DID NOT raise a `ValueError`.
Let's change the function in `src/vehicle_module/horn_noises.py` to the following:

```python
def honk_horn(times=1):
    if times < 1:
        raise ValueError("Times must be at least 1")
    return "Honk! " * times

```

Running the tests again, we can see that all the tests pass.

### Edge Cases / Test Driven Development

So we came up with a couple different ways that the `honk_horn` function might fail, based on
different inputs, and we want to make sure our code handles these cases. We could edit the code file
first, then write the tests, but a more common practice is to write the tests first, and then edit
the code to make the tests pass. This is called "Test Driven Development" (TDD) and has a couple of
benefits:

- 1. It forces us to think about the different ways our code might fail, and how we want to handle
       those cases ahead of time. (e.g. what should happen if the user provides a value of 0 for
       the `times` parameter in the `honk_horn` function?)
- 2. It gives us a safety net of tests that we can run after we make changes to our code, to make
       sure we didn't break anything. (e.g. if we change the `honk_horn` function to raise a
       `ValueError` for a value of 0, we can run our tests to make sure that the function still
       works as expected for other values.)
- 3. It mimics the process for bug hunting - we can write a test that reproduces the bug, then edit
     the code to fix the bug, and then run the tests to make sure the bug is fixed and that we
     didn't break anything else.

Let's add an additional test for the `honk_horn` function that check for one of the edge cases
we discussed earlier:

```python
def test_honk_horn_large_number():
    with pytest.raises(ValueError):
        vehicle_module.horn_noises.honk_horn(11)
```

Run the tests again:

```bash
uv run pytest
```

And we should get a message that our test failed, because the `honk_horn` function did not raise a
`ValueError` for a value of 11. Let's update the `honk_horn` function to the following:

```python
def honk_horn(times=1):
    if times < 1:
        raise ValueError("Times must be at least 1")
    if times > 10:
        raise ValueError("Times must be at most 10")
    return "Honk! " * times
```

::: callout

What about some of the other edge cases we discussed earlier?

Well, let's add them:

```python
def test_honk_horn_non_integer():
    with pytest.raises(TypeError):
        vehicle_module.horn_noises.honk_horn("Two")


def test_honk_horn_negative():
    with pytest.raises(ValueError):
        vehicle_module.horn_noises.honk_horn(-1)
```

And run our tests again. They...pass?

When python tries to multiple a string by a float, a negative integer, or another string, it will
already raise a `TypeError` or `ValueError`. While we could add additional tests for these cases,
it is not strictly necessary, as this functionality is implemented in the Python language itself.

It's very easy to find yourself drowning in tests, and writing tests for each and every possible
edge case. This can even be counterproductive, as it can make it difficult to maintain your tests,
and can slow down your overall development process.

:::


### Testing Classes

So that works well enough for the basic functions we wrote at the start, but what about testing
the classes we made? The Vehicle, Car, GasolineCar and ElectricCar classes? We can test classes
similarly to functions, by writing test functions that create instances of the class and check their
behavior. Let's start by looking at the test cases we wrote previously.

First off, we need to rename the file so that pytest can recognize it as a test file. Let's rename
it to `test_car.py`.

We want our tests to ensure that we are able to create a Car object, and that the methods on the
Car object operate as expected on an instance.

```python
from vehicle_module.car import Car, ElectricCar, GasolineCar

# ... existing code

# Check that we can create a Car object
car = Car(make="Toyota", model="Corolla", year=2020)
if car.make == "Toyota" and car.model == "Corolla" and car.year == 2020:
    passed_tests += 1
else:
    failed_tests += 1

# Test the methods
if car.honk_horn() == "Honk! Honk!":
    passed_tests += 1
else:
    failed_tests += 1

if car.make_engine_noise() == "putt putt":
    passed_tests += 1
else:
    failed_tests += 1
```

In pytest form, this would look like the following:

```python
def test_car():
    my_car = Car(make="TestMake", model="TestModel", year=2026)

    assert my_car.make == "TestMake"
    assert my_car.model == "TestModel"
    assert my_car.year == 2026
    assert my_car.color == "grey"
    assert my_car.fuel == "gasoline"


def test_car_noises():
    my_car = Car(make="TestMake", model="TestModel", year=2026)

    assert my_car.honk_horn() == "Honk! Honk!"
    assert my_car.make_engine_noise() == "putt putt"
```

Note that we can use as many asserts as we like in each test function. If any one of the asserts
fails, the test will fail.

### Fixtures

One of the strengths of pytest is the ability to create fixtures, which are reusable bits of code
that can be used to quickly set up objects or data for our tests. For example, notice that in each
of our tests so far, we have had to create a new instance of the `Car` object with the same set of
parameters. As programmers, we are lazy! And this also could potentially create problems down the
line - what if we have a series of tests, all of which create a new `Car` object, and then one day
we decide to change the parameters of the `Car` object? We would have to edit each test
individually, which is tedious and error-prone. Instead, we can create a fixture that creates a
`Car` object for us, and then we can use that fixture in our tests.

::: callout

Fixtures are special functions in pytest, but they are simple functions in the end. There's nothing
stopping you from just creating a function that returns a `Car` object, and then calling that
function in your tests. The difference is that fixtures are automatically discovered by pytest,
allowing us to create session-level fixtures that need to be used everywhere, module level fixtures
that are used in multiple test files, etc. Fixtures can also be set to be automatically applied, so
we don't have to explicitly include them in our test functions.

:::

Let's create a fixture for our `Car` object. We're using a fixture that comes from `pytest` called
`@pytest.fixture`, so we'll need to add an import to the top of the file:

```python
import pytest
```
Then, add the following code below the imports:

```python
@pytest.fixture
def my_car():
    return Car(make="Toyota", model="Corolla", year=2020)
```

Now, we can use this fixture in our tests. Update the test functions to accept a parameter called
`my_car`, and remove the line that creates the `Car` object. The updated test file
should look like this:

```python
import pytest

from vehicle_module.car import Car, ElectricCar, GasolineCar

@pytest.fixture
def my_car():
    return Car(make="Toyota", model="Corolla", year=2020)

def test_car(my_car):
    assert my_car.make == "Toyota"
    assert my_car.model == "Corolla"
    assert my_car.year == 2020
    assert my_car.color == "grey"
    assert my_car.fuel == "gasoline"


def test_car_noises(my_car):
    assert my_car.honk_horn() == "Honk! Honk!"
    assert my_car.make_engine_noise() == "putt putt"
```

Let's run our tests again with `uv run pytest`. Hopefully, all of our tests are still passing.

### Monkey Patching

Another useful feature of pytest is monkey patching. Monkey patching is a way to modify or extend
the behavior of a function or class during testing. This is useful when you want to test a function
that depends on an external resource, such as a database, file system or web resource. Instead of
actually accessing the external resource, you can use monkey patching to replace the function that
accesses the resource with a mock function that returns a predefined value.

Remember in the last episode when we added our Car glyphs? Let's write a simple check to make sure
that we are getting the correct glyph.


 Now in our test file, we can write a test that checks that the glyph is the correct size. However,
 we don't really want to have to ensure that there is a file called `car.glyph` in the correct
 location, instead we'll use monkey patching to replace the `open` function with a mock function
 that returns a string that we define for the test. This way, we can test the behavior of the
 `glyph` property and how it handles the contents of the file.

 Let's add update our tests in `test_car.py` to include a test for the glyph. First, we need to add
 an import for the `mock_open` at the top of the file:

```python
from unittest.mock import mock_open
```

::: callout

Wait, why are we using `unittest.mock`? I thought we were using `pytest`? `pytest` is a great
testing framework, but it works well with the built-in `unittest.mock` library, which is part of
the Python standard library. `unittest.mock` provides a way to create mock objects and functions
that can be used in tests.

`pytest` does have its own mocking library called `pytest-mock`, but it is not part of the standard
library, and is not included in the default `pytest`. We aren't going to cover this here.

:::

To use this in our test, we need to update our test to "monkeypatch" the `open` function. When our
test tries to run the `glyph` property, it will try to open the file `car.glyph`, but instead of
actually opening the file, it will use our mock function that returns a string that we define for
the test. Our test looks like this:

```python
def test_car_glyph(my_car, monkeypatch):
    file_content = """
1234567890
1234567890
1234567890
1234567890
"""
    mock = mock_open(read_data=file_content)
    monkeypatch.setattr("builtins.open", mock)

    assert isinstance(my_car.glyph, str)
    assert my_car.glyph == file_content.strip()
```

::: instructor

Strictly speaking, I think it would be better to test the glyph property in a separate test file,
like `test_vehicle.py`. We can mention this.

:::


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Write a simple test

Create a file called `text_utilities.py` in the `src/textanalysis_tool` directory. In this file,
paste the following function:


```python
def create_acronym(phrase: str) -> str:
    """Create an acronym from a phrase.

    Args:
        phrase (str): The phrase to create an acronym from.

    Returns:
        str: The acronym.
    """
    if not isinstance(phrase, str):
        raise TypeError("Phrase must be a string.")

    words = phrase.split()
    if len(words) == 0:
        raise ValueError("Phrase must contain at least one word.")

    articles = {"a", "an", "the", "and", "but", "or", "nor", "on", "at", "to", "by", "in"}

    acronym = ""
    for word in words:
        if word.lower() not in articles:
            acronym += word[0].upper()

    return acronym
```

Create the following test cases for this function:

- A test that checks if the acronym for "As Soon As Possible" is "ASAP" and that the acronym for
    "For Your Information" is "FYI".
- A test that checks that the function raises a `TypeError` when the input is not a string.
- A test that checks that the function raises a `ValueError` when the input is an empty string.

Are there any other edge cases you can think of? Write a test to prove that your edge case is not
handled by this function as it is currently written.

::: hint

Remember that to use pytest, you need to create a file that starts with `test_` and that the test
functions need to start with `test_` as well.

:::

::: hint

You can use the `pytest.raises` context manager to check for specific exceptions. For example:

```python
def test_raises_error():
    with pytest.raises(FileNotFoundError):
        read_my_file("non_existent_file.txt")
```

:::

::: hint

What happens if the phrase contains only articles? For example, "and the or by"?

:::

:::::::::::::::: solution

in the `tests` directory, create a file called `test_text_utilities.py`:

```python
import pytest

from textanalysis_tool.text_utilities import create_acronym


def test_create_acronym():
    assert create_acronym("As Soon As Possible") == "ASAP"
    assert create_acronym("For Your Information") == "FYI"


def test_create_acronym_invalid_type():
    with pytest.raises(TypeError):
        create_acronym(123)


def test_create_acronym_empty_string():
    with pytest.raises(ValueError):
        create_acronym("")


def test_create_acronym_no_valid_words():
    with pytest.raises(ValueError):
        create_acronym("and the or")

```

Run the tests with `uv run pytest`.

In the `create_acronym` function, we need to add a check after we finish iterating through the
words to see if the acronym is empty. If it is, we can raise a `ValueError`:

```python
    ...

    if not acronym:
        raise ValueError("Phrase must contain at least one non-article word.")

    return acronym
```


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Additional Edge Case

Try adding a test for another edge case for our Document class, this time for a file that is not
actually a text file, for example, a binary file or an image file. Then, update the `Document`
class to make the test pass.

::: hint

You can mock a binary file by using the `mock_open` function from the `unittest.mock` module, and
using the `read_data` parameter to provide binary data like `b'\x00\x01\x02'`.

:::

::: hint

In the `Document` class, we need to check if the data read from the file is binary data. The `read`
method of a file object is clever enough to return binary data as a `bytes` object, so we can check
if the data in `self._content` is an instance of type `bytes`. If it is, we can raise a
`ValueError`.

```python
text_data = "This is a test string."
if isinstance(text_data, bytes):
    raise ValueError("File is not a valid text file.")

binary_data = b'\x00\x01\x02'
if isinstance(binary_data, bytes):
    raise ValueError("File is not a valid text file.")
```

:::

:::::::::::::::: solution

You can create a test that simulates opening a binary file by using the `mock_open` function from
the `unittest.mock` module. Here's an example of how you might write such a test:

```python
def test_binary_file(monkeypatch):
    # Mock a binary file
    mock = mock_open(read_data=b'\x00\x01\x02')
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        Document(filepath="binary_file.bin")
```

And then, in the `Document` class, you can check if the data read from the file is binary data like
this:

```python
...
    def get_content(self, filepath: str) -> str:
        raw_text = self.read(filepath)
        if not raw_text:
            raise ValueError(f"File {filepath} contains no content.")

        if isinstance(raw_text, bytes):
            raise ValueError(f"File {self.filepath} is not a valid text file.")

        match = re.search(self.CONTENT_PATTERN, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"File {filepath} is not a valid Project Gutenberg Text file.")
...
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

- We can use `pytest` to write and run unit tests in Python.
- A good test is isolated, repeatable, fast, and clear.
- We can use fixtures to provide data or state to our tests.
- We can use monkey patching to modify the behavior of functions or classes during testing.
- Test Driven Development (TDD) is a practice where we write tests before writing the code to
  make the tests pass.

::::::::::::::::::::::::::::::::::::::::::::::::
