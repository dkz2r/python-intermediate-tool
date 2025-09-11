---
title: 'Class Objects'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What is a class object?
- How can I defined a class object in Python?
- How can I use a class object in my module?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Create a Class object in our module.
- Demonstrate how to use our Class object in a sample script.

::::::::::::::::::::::::::::::::::::::::::::::::

## What is a Class Object?

You can think of a class object as a kind of "blueprint" for an object. It defines what properties
the object can have, and what methods it can perform. Once a class is defined, you can create any
number of objects based on that class, each of which is referred to as an "instance" of that class.

As an example, let's imagine a Car. A Car has many properties and can do many things, but for our
purposes, let's limit them slightly. Our Car will have a make, model, year, and color, and it will
be able to honk, and be painted.

The make, model, year, and color are all "properties" of the car. Honking a horn and being painted
are both "methods" of the car. Here's a diagram of our car object:

![Car Class object example](./fig/03-class-objects/car_class.PNG){alt='Car Class object example'}

In python we can define a class object like this:

```
class Car:
    def __init__(self, make: str, model: str, year: int, color: str = "grey"):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def honk(self) -> str:
        return "beep"

    def paint(self, new_color: str) -> None:
        self.color = new_color
```

::: callout

The convention in python is that all classes should be named in CamelCase, with no underscores.
Class names in reality can be anything you like, but this is the standard in the python community.

:::


Some of this might look familiar if you think about how we define functions in Python. There's a
`def` keyword, followed by the function name and parentheses. Inside the parentheses, we can define
parameters, and these parameters can contain default values. We can also include type hints, for
both parameters and return values. However all of this is indented one level, underneath the
`class` keyword, which is followed by our class name.

Note that this is just our blueprint - it doesn't refer to any specific car, just the general idea
of a car. Also note the `__init__` method. This is a special method which is called whenever you
"instantiate" a new object. The parameters for this function are supplied when we first create an
object and function similarly to a method, in that if no default value is provided, it is required
in order to create the object, and if a default value is provided, it is optional.

An instance of a car, in this case called "my_car" might look something like this:

![Car Instance Example](./fig/03-class-objects/car_instance.PNG){alt='Car Instance example'}

Also note that each of the methods within the class object definition starts with a "self"
argument. This is a reference to the current instance of the class, and is used to access
variables that belong to the class. In our example, we store the make, model, year and color as
properties of the class. When we call the `paint` method, we use `self.color` to refer to the
current instance's color property.

::: callout

The `__init__` method is called a "dunder" (double underlined) method in python. There are a number
of other dunder methods that we can define, that will interact with various built-in functions and
operators. For example, we can define a `__str__` method, that will allow us to specify how our
object should be represented as a string when we call `str()` on it. Likewise, we can define
`__eq__`, which would tell python how to behave when we compare two objects for equality.

:::

## A Class object for Our project

Let's create a class object for our text analysis project. We're going to be downloading some books
from [Project Gutenberg](https://www.gutenberg.org/). To make things easy to begin with, we'll
limit ourselves to just the .txt files.

Since we're going to create some useful objects and methods for working with documents, let's
define a `Document` class.

::: discussion

Take a look a an example txt document from Project Gutenberg:
[Meditations, by Marcus Aurelius](https://www.gutenberg.org/cache/epub/2680/pg2680.txt)

What properties and methods might we want to include in our Document class?

:::

It looks like there's a standard metadata section in these documents, with a Title, Author, Release
Date, Language, and Credits. Those will probably be useful metadata. Looking at the url for this
file, it also looks like there's an ID on Project Gutenberg.

For methods, we'll need to be able to read the document from a file. And for some simple methods,
let's count the number of lines in a document, and another method to get the number of times a
particular word appears.

Lets start writing our class object in a new file: `src/textanalysis_tool/document.py`:

```python

class Document:
    def __init__(self, filepath: str, title: str, author: str = "", id: int = 0):
        self.filepath = filepath
        self.title = title
        self.author = author
        self.id = id
        self._content = self._read(self.filepath)

    def _read(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_line_count(self) -> int:
        return len(self._content.splitlines())

    def get_word_occurrence(self, word: str) -> int:
        return self._content.lower().count(word.lower())
```

Our class object `Document` is a "blueprint" for a collection of methods. When we define it, we
have to provide the class with a filepath, a title, an author, and an id. Only the filepath and the
title are required, while the author and id are optional.

The `__init__` method is called as soon as the object is created, and we can see that in addition
to storing the parameters to their `self` counterparts, there is an additional property called
`self._content`. This property is used to store the entire text content of the document. We obtain
this by calling the `self._read` method, which reads the content from the specified file.

::: callout

## Principle of Least Astonishment (or, We're All Adults Here)

Unlike other programming languages, python doesn't have the concept of "private" or "internal"
variables and methods. Instead there is a convention which says that any variable or method that is
intended for internal use should be prefixed with an underscore (e.g. `_content`). This is however
just a convention - there is nothing stopping you from accessing these variables and methods from
outside the class if you really want to.

:::

There are also two methods that we've defined - `get_line_count` and `get_word_occurrence`. Neither
of these will be called directly on the class itself, but rather on instances of the class that we
create (as indicated by the use of `self` within the class methods). Note that these methods make
use of the `self._content` property - this is a variable that is not defined within the method,
so you may expect it to be out of scope. However the `self` keyword refers to the specific instance
of the class itself, and so it has access to all of its properties and methods, including the
`self._content` property.

## Trying out Our Class Object

Let's try out our new class object. Create a file in our "tests" directory called
`example_file.txt` and add some text to it:

```
This is a test document. It contains words.
It is only a test document.
```

Next, let's create another test file. Our last one was called `test_my_modue.py`, so let's call this
`test_document.py`:

```python
import sys

sys.path.insert(0, "./src")

from textanalysis_tool.document import Document

total_tests = 3
passed_tests = 0
failed_tests = 0

# Check that we can create a Document object
doc = Document(filepath="tests/example_file.txt", title="Test Document")
if doc.title == "Test Document" and doc.filepath == "tests/example_file.txt":
    passed_tests += 1
else:
    failed_tests += 1

# Test the methods
if doc.get_line_count() == 2:
    passed_tests += 1
else:
    failed_tests += 1

if doc.get_word_occurrence("test") == 2:
    passed_tests += 1
else:
    failed_tests += 1

print(f"Total tests: {total_tests}")
print(f"Passed tests: {passed_tests}")
print(f"Failed tests: {failed_tests}")
```

Now we'll run this file using our uv environment:

```bash
uv run tests/test_document.py
```

You should see the output:

```
Total tests: 3
Passed tests: 3
Failed tests: 0
```


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Testing Out Our Class on Real Data

Let's download a real text file from Project Gutenberg and see how our class object handles it.
You can pick any file you like, or you can use the same one we looked at earlier:
[Meditations, by Marcus Aurelius](https://www.gutenberg.org/cache/epub/2680/pg2680.txt).

Modify your `test_document.py` file to create a new Document object using the real text file,
and then test out the `get_line_count` and `get_word_occurrence` methods on it. What do you get?
What issues might there be when we start using this class on our actual data?

How can we improve our class to handle these issues?

::: hint

The Metadata at the start of the document is always gated by a line that says
`*** START OF THE PROJECT GUTENBERG EBOOK {the title of the book} ***` and at the end of the
document with the line `*** END OF THE PROJECT GUTENBERG EBOOK {the title of the book} ***`.

:::

::: hint

There is a python module called `re` that allows us to work with regular expressions. This can be
used to match specific patterns in text, or for extracting specific parts of a string. You can
use the following regex pattern to match the content between the start and end markers:

```python
pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
```

:::

:::::::::::::::: solution

The Project Gutenberg text files have a lot of metadata at the start and end of the file, which
will affect the line count and word occurrence counts. We might want to modify our `_read` method
to strip out this metadata before storing the content in `self._content`.

One possible solution would look like this:

```python

import re

class Document:

    CONTENT_PATTERN = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    def __init__(self, filepath: str, title: str, author: str = "", id: int = 0):
        self.filepath = filepath
        self.title = title
        self.author = author
        self.id = id
        raw_text = self._read(self.filepath)

        if not raw_text:
            raise ValueError(f"File {self.filepath} contains no content.")

        self._content = self._get_content(raw_text)


    def _get_content(self, content: str) -> str:
        match = re.search(self.CONTENT_PATTERN, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"File {self.filepath} is not a valid Project Gutenberg Text file.")

    def _read(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_line_count(self) -> int:
        return len(self._content.splitlines())


    def get_word_occurrence(self, word: str) -> int:
        return self._content.lower().count(word.lower())

```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Extracting the Metadata

From the previous challenge, we saw that the Project Gutenberg text files have a lot of metadata
at the start and end of the file. This metadata includes the title, author, release date, and other
information about the book which we currently are adding to our file using parameters.

Instead of passing this information in as parameters, can you modify the class so that it extracts
the title, author and id from the metadata in the text file itself?

::: hint

As before, we can use the `re` module to extract this information. The title and author are
contained in lines that start with `Title:` and `Author:` respectively. The ID can be found in the
line that starts with `Release Date:`. You can use the following regex patterns to match these
lines:

```python
TITLE_PATTERN = r"^Title:\s*(.*?)\s*$"
AUTHOR_PATTERN = r"^Author:\s*(.*?)\s*$"
ID_PATTERN = r"^Release date:\s*.*?\[eBook #(\d+)\]"
```

:::

:::::::::::::::: solution

There's any number of ways to do this, but one possible solution would look like this:

```python

import re

class Document:

    TITLE_PATTERN = r"^Title:\s*(.*?)\s*$"
    AUTHOR_PATTERN = r"^Author:\s*(.*?)\s*$"
    ID_PATTERN = r"^Release date:\s*.*?\[eBook #(\d+)\]"
    CONTENT_PATTERN = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    def __init__(self, filepath: str):
        self.filepath = filepath
        raw_text = self._read(self.filepath)

        if not raw_text:
            raise ValueError(f"File {self.filepath} contains no content.")

        self.title = self._get_metadata(raw_text, self.TITLE_PATTERN)
        self.author = self._get_metadata(raw_text, self.AUTHOR_PATTERN)
        extracted_id = self._get_metadata(raw_text, self.ID_PATTERN)
        self.id = int(extracted_id) if extracted_id else None

        self._content = self._get_content(raw_text)


    def _get_content(self, content: str) -> str:
        match = re.search(self.CONTENT_PATTERN, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"File {self.filepath} is not a valid Project Gutenberg Text file.")

    def _get_metadata(self, content: str, pattern: str) -> str | None:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    def _read(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_line_count(self) -> int:
        return len(self._content.splitlines())


    def get_word_occurrence(self, word: str) -> int:
        return self._content.lower().count(word.lower())

```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Properties

In our current implementation, the `title`, `author`, and `id` attributes are publicly accessible
from outside the class, which means that they can be modified directly. There are instances where
it might be preferable for the attributes to be read-only, so that they can only be set when the
object is created, and not modified afterwards, or to allow us to create variables that are based
or calculated from other variables and should not be set directly.

We can do this with the `@property` decorator. This is a special decorator that allows us to define
"getter" and "setter" methods for a property. It works much the same as a normal method, but it is
accessed like an attribute.

We can convert our `get_line_count` method to a property like this:

```python
    ...

    @property
    def line_count(self) -> int:
        return len(self._content.splitlines())

    ...
```

The links to the project gutenberg files are based on the id, which we extracted from the metadata.
Create a new property called `gutenberg_url` that returns the url for the document based on the id.

::: hint

The url for a Project Gutenberg text file is of the form:
`https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt`

:::

:::::::::::::::: solution

There's any number of ways to do this, but one possible solution would look like this:

```python

    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

```

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::

Neat! We've successfully created and used a class object in our module. But certainly there's a
better way to test this, right? In the next episode, we'll look at how to write proper unit tests
for our class object with `pytest`.

::::::::::::::::::::::::::::::::::::: keypoints

- foo

::::::::::::::::::::::::::::::::::::::::::::::::

