---
title: '05-extending-classes'
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
        with open("pg2680-images.html", encoding="utf-8") as file_obj:
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

Now let's try testing out our classes. We already have the `pg2680.txt` file in our ´scratch´
folder, now let's download the HTML version of the same book from Project Gutenberg. You can
download it from [this link](https://www.gutenberg.org/cache/epub/55317/pg55317-h.zip). (Note
that the file is zipped, as it also contains images. We won't be using the images, but you'll need
to unzip the file to get to the HTML file.) Once you have the HTML file, place it in the ´scratch´
folder alongside the ´pg2680.txt´ file.

You can either copy and paste the code below into a new file called `test_inheritance.py`, or you
can download the file from the [Workshop Resources TODO]().

```python
import sys
sys.path.insert(0, "./src")


´´´

::::::::::::::::::::::::::::::::::::: keypoints

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

::::::::::::::::::::::::::::::::::::::::::::::::

