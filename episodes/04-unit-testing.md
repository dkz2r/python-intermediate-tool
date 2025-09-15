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

We have our two little test files, but you might imagine that it's not particuarly efficient to
always write individual scripts to test our code. What if we had a lot of functions or classes?
Or a lot of different ideas to test? What if our objects changed down the line? Our existing
modules are going to be diffucult to maintain, and, as you may have expected, there is alredy a
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

What are some edge cases that you can think of for the `hello` function we wrote earlier?

What about the `Document` class?

:::

::: spoiler

Some edge cases for the `hello` function could include:

- Passing in an empty string
- Passing in a very long string
- Passing in something that is not a string (e.g. a number or a list)

Some edge cases for the `Document` class could include:

- Passing in a file path that does not exist
- Passing in a file that is not a text file
- Passing in a file that is empty
- Passing in a word that does not exist in the document when testing `get_word_occurrence`

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
    "pytest>=8.4.2",
]
```

Now we can start creating our tests.

### Writing a pytest Test File

Part of `pytest` is the concept of "test discovery". This means that pytest will automatically find
any test files that follow a certain naming convention. By default, pytest will look for files
that start with `test_` or end with `_test.py`. Inside these files, pytest will look for functions
that start with `test_`.

Now, our files already have the correct names, so we just need to change the contents. Let's start
with `test_say_hello.py`. Open it up and replace the contents with the following:

```python
from textanalysis_tool.say_hello import hello

def test_hello():
    assert hello("My Name") == "Hello, My Name!"
```

In our previous test file, we had to add the path to our module each time. Now that we are using
`pytest`, we can use a special file called `conftest.py` to add this path automatically. Create a
file called `conftest.py` in the `tests` directory and add the following code to it:

```python
import sys

sys.path.insert(0, "./src")
```

::: instructor

This is how I always do it, but I assume there's a better way.

:::

Now, we just need to run the tests. We can do this with the following command:

```bash
uv run pytest
```

::: callout

Note that we are using `uv run` to run pytest, this ensures that pytest is run in the correct
environment with all the dependencies we have installed.

:::

You should see output similar to the following:

```
============================= test session starts ==============================
platform win32 -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: D:\Documents\Projects\textanalysis-tool
configfile: pyproject.toml
collected 1 item

tests\test_say_hello.py .                                          [100%]
============================== 1 passed in 0.12s ===============================
```

Why didn't it run the other test file? Because even though the file is named correctly, it
doesn't contain any functions that start with `test_`. Let's fix that now.

Open up `test_document.py` and replace the contents with the following:

```python
from textanalysis_tool.document import Document

def test_create_document():
    Document.CONTENT_PATTERN = r"(.*)"
    doc = Document(filepath="tests/example_file.txt")
    assert doc.filepath == "tests/example_file.txt"


def test_document_word_count():
    Document.CONTENT_PATTERN = r"(.*)"
    doc = Document(filepath="tests/example_file.txt")
    assert doc.get_line_count() == 2


def test_document_word_occurrence():
    Document.CONTENT_PATTERN = r"(.*)"
    doc = Document(filepath="tests/example_file.txt")
    assert doc.get_word_occurrence("test") == 2
```

::: callout

Our example file doesn't exactly look like a Project Gutenberg text file, so we need to change the
`CONTENT_PATTERN` to match everything. This is a class level variable, so we can change it on the
class itself, rather than on the instance.

:::

Let's run our tests again:

```bash
uv run pytest
```

You should see output similar to the following:

```
============================= test session starts ==============================
platform win32 -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: D:\Documents\Projects\textanalysis-tool
configfile: pyproject.toml
collected 4 items

tests\test_document.py ...                                      [ 75%]
tests\test_say_hello.py .                                       [100%]
============================== 4 passed in 0.15s ===============================
```

You can see that all of the tests have passed. There is a small green pip for each test that was
performed, and a summary at the end. Compare this to the test file we had before. We got rid of all
of the if statements, and just use the `assert` statement to check if the output is what we expect.

### Testing Edge Cases / Exceptions

Let's add an edge case to our tests. Open up `test_say_hello.py` and add a test case for an empty
string:

```python
from textanalysis_tool.say_hello import hello

def test_hello():
    assert hello("My Name") == "Hello, My Name!"

def test_hello_empty_string():
    assert hello("") == "Hello, !"
```

Run the tests again:

```bash
uv run pytest
```

We get passing tests, which is what we expect. But we are the ones in charge of the function, what
if we say that if the user doesn't provide a name, we want to raise an exception? Let's change the
test to say that if the user provides an empty string, we want to raise a `ValueError`:

```python
import pytest

from textanalysis_tool.say_hello import hello


def test_hello():
    assert hello("My Name") == "Hello, My Name!"


def test_hello_empty_string():
    with pytest.raises(ValueError):
        hello("")

```

Run the tests again:

```bash
uv run pytest
```

This time, we get a failing test, because the `hello` function DID NOT raise a `ValueError`. Let's
change the `hello` function to raise a `ValueError` if the name is an empty string:

```python
def hello(name: str = "User"):
    if name == "":
        raise ValueError("Name cannot be empty")
    return f"Hello, {name}!"
```

Running the tests again, we can see that all the tests pass.

### Fixtures

One of the great features of pytest is the ability to use fixtures. Fixtures are a way to provide
data, state or configurations to your tests. For example, we have a line in each of our tests that
creates a new `Document` object. We can use a fixture to create this object once, and then use it
in each of our tests. That way, if we need to change the way we create the object in the future, we
only need to change it in one place.

Let's create a fixture for our `Document` object. Open up `test_document.py` and add the following
import at the top:

```python
import pytest
```
Then, add the following code below the imports:

```python
@pytest.fixture
def doc():
    return Document(filepath="tests/example_file.txt")
```

Now, we can use this fixture in our tests. Update the test functions to accept a parameter called
`doc`, and remove the line that creates the `Document` object. The updated test file
should look like this:

```python
import pytest

from textanalysis_tool.document import Document

@pytest.fixture
def doc():
    Document.CONTENT_PATTERN = r"(.*)"
    return Document(filepath="tests/example_file.txt")

def test_create_document(doc):
    assert doc.title == "Test Document"
    assert doc.filepath == "tests/example_file.txt"

def test_document_word_count(doc):
    assert doc.get_line_count() == 2

def test_document_word_occurrence(doc):
    assert doc.get_word_occurrence("test") == 2
```

::: callout

Because our Documents are validated by searching for a starting and ending regex pattern, our test
files will not have that. We could ensure that our test files would, or we can just temporarily
alter the search pattern for the duration of the test. `CONTENT_PATTERN` is a class level variable,
so we need to modify it before the instance is created.

:::

Let's run our tests again. Nothing changed in the output, but our code is now cleaner and easier
to maintain.

### Monkey Patching

Another useful feature of pytest is monkey patching. Monkey patching is a way to modify or extend
the behavior of a function or class during testing. This is useful when you want to test a function
that depends on an external resource, such as a database, file system or web resource. Instead of
actually accessing the external resource, you can use monkey patching to replace the function that
accesses the resource with a mock function that returns a predefined value.

In our use case, we have a file called `example_file.txt` that we use to test our `Document`
class. However, if we wanted to test the `Document` class with files that have different contents,
would need to create a whole array of different test files. Instead, we can use monkey patching to
replace the `open` function, so that instead of actually opening a file, it returns a string that
we define.

Let's monkey patch the `open` function in our `test_document.py` file. First, we need to import the
`monkeypatch` fixture from `unittest.mock` (a python built-in module). Add the following import at
the top of the file:

```python
from unittest.mock import mock_open
```

Then, we can create a new fixture that monkey patches the `open` function. Add the following code
below the `doc` fixture:

```python
@pytest.fixture(autouse=True)
def mock_file(monkeypatch):
    mock = mock_open(read_data="This is a test document. It contains words.\nIt is only a test document.")
    monkeypatch.setattr("builtins.open", mock)
    return mock
```

The other difference you'll notice is that we added the parameter `autouse=True` to the fixture.
This means that, within this test file, this specific fixture will be automatically applied to all
tests, without needing to explicitly include it as a parameter in each test function.

Go ahead and delete the `example_file.txt` file, and run the tests again. Your tests should still
pass, even though the file doesn't exist anymore. This is because we are using monkey patching to
replace the `open` function with a mock function that returns the string we defined.

### Edge Cases Again / Test Driven Development

Let's go back and think about other things that might go wrong with our `Document` class. What if
the user provides a file path that doesn't exist? What if the user provides a file that is not a
text file? Or a file that is empty of content? Rather than write these into our class object, we
can first write tests that will check for the behavior we expect or want in these edge cases, see
if they fail, and then update our class object to make the tests pass. This is called "Test Driven
Development" (TDD), and is a common practice in software development.

Let's add a test for a file that is empty. In this case, we would want the initialization of the
object to fail with a `ValueError`. However for this test, we can't use our fixtures from above, so
we'll have to code it into the test. Add the following to `test_document.py`:

```python
def test_empty_file(monkeypatch):
    # Mock an empty file
    mock = mock_open(read_data="")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        Document(filepath="empty_file.txt")
```

::: callout

Because we are monkeypatching the `open` function, we don't actually need to have a file called
`empty_file.txt` in our tests directory. The `open` function will be replaced with our mock
function that returns an empty string. We are providing a file name here to be consistent with the
`Document` class initialization, and we are using the name to act as additional information for
later developers to clarify the intent of the test.

:::

Run the tests again:

```bash
uv run pytest
```

It fails, as we expect. Now, let's update the `Document` class to raise a `ValueError` if the file
is empty. Open up `document.py` and update the `__init__` method to the following:

```python
def __init__(self, filepath: str, title: str = "Untitled Document"):
    self.filepath = filepath
    self.title = title
    with open(filepath, 'r') as file:
        self._content = file.read()
    if not self._content:
        raise ValueError(f"File {self.filepath} contains no content.")
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Additional Edge Case

Try adding a test for another edge case, this time for a file that is not actually a text file, for
example, a binary file or an image file. Then, update the `Document` class to make the test pass.

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
class Document:
    def __init__(self, filepath: str, title: str, author: str = "", id: int = 0):
        self.filepath = filepath
        self.title = title
        self.author = author
        self.id = id
        self._content = self._read(self.filepath)

        if not self._content:
            raise ValueError(f"File {self.filepath} contains no content.")

        if isinstance(self._content, bytes):
            raise ValueError(f"File {self.filepath} is not a valid text file.")
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
