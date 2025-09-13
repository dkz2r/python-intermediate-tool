---
title: 'Extending Classes with Inheritance'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What if we want classes that are similar, but handle slightly different cases?
- How can we avoid duplicating code in our classes?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the concept of inheritance in object-oriented programming
- Demonstrate how to create a subclass that inherits from a parent class
- Show how to override methods and properties in a subclass

::::::::::::::::::::::::::::::::::::::::::::::::

## Extending Classes with Inheritance

So far you may be wondering why classes are useful. After all, all we've really done in essence is
make a tiny module with some functions in it that are slightly more complicated than normal
functions. One of the real powers of classes is the ability to limit code duplicate through a
concept called inheritance.

### Inheritance

Inheritance is a way to create a new class that contains all of the same properties and methods as
an existing class, but allows us to add additional new properties and methods, or to override
existing methods. This allows us to create a new class that is a specialized version of an existing
class, without having to rewrite a whole bunch of code.

Taking a look at our Car class from earlier, we might want to create a new class for a specific
type of car, like a Convertable Car. A Convertible Car is a type of Car, so it should have
everything that a Car has, but it also has some additional properties and methods, for example, it
might have a property to indicate whether the roof is up or down. We can create a new class called
ConvertibleCar that inherits from the Car class, and then add the new property and method to it.

```python
class ConvertibleCar(Car):
    def __init__(self, make: str, model: str, year: int, color: str = "grey"):
        super().__init__(make, model, year, color)
        self.roof_is_up = True

    def lower_roof(self) -> None:
        self.roof_is_up = False

    def raise_roof(self) -> None:
        self.roof_is_up = True
```

You can see that the ConvertibleCar class is defined in a similar way to the Car class, but it
inherits from the Car class by including it in parentheses after the class name. The `__init__`
method of the ConvertibleCar class also has a call to `super().__init__()`. The `super()` function
is a way to refer specifically to the parent class, in this case, the Car class. This allows us to
call the `__init__` method of the Car class, which sets up all of the properties that a Car has.

### Applying Inheritance to Our Document Class

For our `Document` class, we have a few different types of documents available from the
Project Gutenberg website. We are currently using plain text files, but there are also HTML files
that we can download. They will have the same information, but the data within will be structured
in a slightly different way. We can use inheritance to create a pair of new classes: `HTMLDocument`
and `PlainTextDocument`, that both inherit from the `Document` class. This will allow us to keep
all of the common functionality in the `Document` class, but to add any additional functionality
specific to each document type.

Most of what we've written so far is specific to reading and parsing data out of the plain text
files, so almost all of the code from `Document` can be copied. We'll leave the functions for
`gutenberg_url`, `get_line_count`, and `get_word_occurrence`.

In addition, we'll need an `__init__` in our `Document` class. At the moment, all it does is save
the filename in the `filename` property, but we might expand this in the future. We'll also need a
reference to the `super().__init__()` in our `PlainTextDocument`. At the moment, our classes look
like this:

```python
class Document:
    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_line_count(self) -> int:
        return len(self._content.splitlines())

    def get_word_occurrence(self, word: str) -> int:
        return self._content.lower().count(word.lower())
```

```python
import re

from textanalysis_tool.document import Document

class PlainTextDocument(Document):
    TITLE_PATTERN = r"^Title:\s*(.*?)\s*$"
    AUTHOR_PATTERN = r"^Author:\s*(.*?)\s*$"
    ID_PATTERN = r"^Release date:\s*.*?\[eBook #(\d+)\]"
    CONTENT_PATTERN = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        raw_text = self._read(self.filepath)

        if not raw_text:
            raise ValueError(f"File {self.filepath} contains no content.")

        if isinstance(raw_text, bytes):
            raise ValueError(f"File {self.filepath} is not a valid text file.")

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
```

We'll also have another class for reading HTML files. This will be similar to the
´´PlainTextDocument´´ class, but it will use the ´BeautifulSoup´ library to parse the HTML file and
extract the content and metadata. Rather than type out the entire class now, you can either copy
and paste the code below into a new file called ´html_document.py´, or you can download the file
from the [Workshop Resources TODO]().

::: spoiler

´´´python
import re

from bs4 import BeautifulSoup

from textanalysis_tool.document import Document

class HTMLDocument(Document):
    URL_PATTERN = "^https://www.gutenberg.org/files/(\d+)/.*"

    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}-h.zip"
        return None

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        raw_soup = self._read(self.filepath)

        self.title = self._get_metadata(raw_soup, "dc.title")
        self.author = self._get_metadata(raw_soup, "dc.creator")
        url = self._get_metadata(raw_soup, "dcterms.source")
        extracted_id = re.search(self.URL_PATTERN, url, re.DOTALL)
        self.id = int(extracted_id.group(1)) if extracted_id.group(1) else None

        self._content = self._get_content(raw_soup)

    def _read(self, filepath) -> BeautifulSoup:
        with open(filepath, encoding="utf-8") as file_obj:
            soup = BeautifulSoup(file_obj)

        return soup

    def _get_content(self, soup: BeautifulSoup) -> str:
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

        return '\n\n'.join(content)

    def _get_metadata(self, soup: BeautifulSoup, tag_name: str) -> str:
        return soup.find("meta", {"name": tag_name})["content"]
´´´

:::

### Overriding Methods

Notice that in the `HTMLDocument` class, we have overridden the `gutenberg_url` property to return
the URL for the HTML version of the book. This is an example of how we can override methods and
properties in a subclass to provide specialized behavior. When we create an instance of
`HTMLDocument`, it will use the `gutenberg_url` property defined in the `HTMLDocument` class,
rather than the one defined in the `Document` class.

::: callout

When overriding methods, it's important to ensure that the new method has the same signature as
the method being overridden. This means that the new method should have the same name, number of
parameters, and return type as the method being overridden.

Additionally, the `__init__` is technically also an overridden method, since it is defined in the
parent class. However, since we are calling the parent class's `__init__` method using `super()`, we
are not completely replacing the behavior of the parent class's `__init__` method, but rather
extending it. We can do the exact same thing with other methods if we want to add some
functionality to an existing method, rather than completely replacing it.

:::

### Testing our Inherited Classes

Now let's try out our classes. We already have the `pg2680.txt` file in our ´scratch´ folder, now
let's download the HTML version of the same book from Project Gutenberg. You can download it from
[this link](https://www.gutenberg.org/cache/epub/55317/pg55317-h.zip). (Note that the file is
zipped, as it also contains images. We won't be using the images, but you'll need to unzip the file
to get to the HTML file.) Once you have the HTML file, place it in the ´scratch´ folder alongside
the ´pg2680.txt´ file.

You can either copy and paste the code below into a new file called `demo_inheritance.py`, or you
can download the file from the [Workshop Resources TODO]().

```python
import sys

sys.path.insert(0, "src")

from textanalysis_tool.document import Document
from textanalysis_tool.plain_text_document import PlainTextDocument
from textanalysis_tool.html_document import HTMLDocument

# Test the PlainTextDocument class
plain_text_doc = PlainTextDocument(filepath="scratch/pg2680.txt")
print(f"Plain Text Document Title: {plain_text_doc.title}")
print(f"Plain Text Document Author: {plain_text_doc.author}")
print(f"Plain Text Document ID: {plain_text_doc.id}")
print(f"Plain Text Document Line Count: {plain_text_doc.line_count}")
print(f"Plain Text Document 'the' Occurrences: {plain_text_doc.get_word_occurrence('the')}")
print(f"Plain Text Document Gutenberg URL: {plain_text_doc.gutenberg_url}")
print(f"Type of Plain Text Document: {type(plain_text_doc)}")
print(f"Parent Class: {type(plain_text_doc).__bases__[0]}")

print("=" * 40)

# Test the HTMLDocument class
html_doc = HTMLDocument(filepath="scratch/pg2680-images.html")
print(f"HTML Document Title: {html_doc.title}")
print(f"HTML Document Author: {html_doc.author}")
print(f"HTML Document ID: {html_doc.id}")
print(f"HTML Document Line Count: {html_doc.line_count}")
print(f"HTML Document 'the' Occurrences: {html_doc.get_word_occurrence('the')}")
print(f"HTML Document Gutenberg URL: {html_doc.gutenberg_url}")
print(f"Type of HTML Document: {type(html_doc)}")
print(f"Parent Class: {type(html_doc).__bases__[0]}")

print("=" * 40)

# We can't use the Document class directly
doc = Document(filepath="scratch/pg2680.txt")
```

You should get some output that looks like this:

```
Plain Text Document Title: Meditations
Plain Text Document Author: Emperor of Rome Marcus Aurelius
Plain Text Document ID: 2680
Plain Text Document Line Count: 6845
Plain Text Document 'the' Occurrences: 5736
Plain Text Document Gutenberg URL: https://www.gutenberg.org/cache/epub/2680/pg2680.txt
Type of Plain Text Document: <class 'textanalysis_tool.plain_text_document.PlainTextDocument'>
Parent Class: <class 'textanalysis_tool.document.Document'>
========================================
HTML Document Title: Meditations
HTML Document Author: Marcus Aurelius, Emperor of Rome, 121-180
HTML Document ID: 2680
HTML Document Line Count: 5635
HTML Document 'the' Occurrences: 6161
HTML Document Gutenberg URL: https://www.gutenberg.org/cache/epub/2680/pg2680-h.zip
Type of HTML Document: <class 'textanalysis_tool.html_document.HTMLDocument'>
========================================
Parent Class: <class 'textanalysis_tool.document.Document'>
Traceback (most recent call last):
  File "E:\Projects\Python\scratch\textanalysis-tool\scratch\demo_inheritance.py", line 34, in <module>
    doc = Document(filepath="scratch/pg2680.txt")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\Projects\Python\scratch\textanalysis-tool\src\textanalysis_tool\document.py", line 14, in __init__
    self.content = self.get_content(filepath)
                   ^^^^^^^^^^^^^^^^
AttributeError: 'Document' object has no attribute 'get_content'
```

Note that the end of the script results in an error - since the `Document` class is no longer
contains the `get_content` or `get_metadata` methods, it cannot be used directly. However we don't
get an error until we try to call one of those methods.

::: callout

This is a use case for something called an abstract base class, which is a class that is designed
to be inherited from, but never instantiated directly. One way to handle this would be to add these
methods to the `Document` class, but have them raise a `NotImplementedError`. This way, if someone
tries to instantiate the `Document` class directly, they will get an error indicating that maybe
this class is not meant to be used directly:

```python
class Document:
    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

    @property
    def line_count(self) -> int:
        return len(self.content.splitlines())

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = self.get_content(filepath)

        metadata = self.get_metadata(filepath)
        self.title = metadata.get("title")
        self.author = metadata.get("author")
        self.id = metadata.get("id")

    def get_word_occurrence(self, word: str) -> int:
        return self.content.lower().count(word.lower())

    def get_content(self, filepath: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_metadata(self, filepath: str) -> dict[str, str | None]:
        raise NotImplementedError("This method should be implemented by subclasses.")
```

Another way to handle this is to use the `abc` module from the standard library, which provides
a way to define abstract base classes. This is a more formal way to define a class that is meant
to be inherited from, but not instantiated directly:

```python
from abc import ABC, abstractmethod

class Document(ABC):
    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

    @property
    def line_count(self) -> int:
        return len(self.content.splitlines())

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = self.get_content(filepath)

        metadata = self.get_metadata(filepath)
        self.title = metadata.get("title")
        self.author = metadata.get("author")
        self.id = metadata.get("id")

    def get_word_occurrence(self, word: str) -> int:
        return self.content.lower().count(word.lower())

    @abstractmethod
    def get_content(self, filepath: str) -> str:
        pass

    @abstractmethod
    def get_metadata(self, filepath: str) -> dict[str, str | None]:
        pass
```

:::

::::::::::::::::::::::::::::::::::::: keypoints

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

::::::::::::::::::::::::::::::::::::::::::::::::

