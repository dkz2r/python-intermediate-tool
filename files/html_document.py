import re

from bs4 import BeautifulSoup

from textanalysis_tool.document import Document

class HTMLDocument(Document):
    URL_PATTERN = "^https://www.gutenberg.org/files/([0-9]+)/.*"

    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}-h.zip"
        return None

    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        parsed_file = self._read(self.filepath)

        self.title = self._get_metadata(parsed_file, "dc.title")
        self.author = self._get_metadata(parsed_file, "dc.creator")
        url = self._get_metadata(parsed_file, "dcterms.source")
        extracted_id = re.search(self.URL_PATTERN, url, re.DOTALL)
        self.id = int(extracted_id.group(1)) if extracted_id.group(1) else None

        self._content = self._get_content(parsed_file)

    def read(self, filepath) -> BeautifulSoup:
        with open(filepath, encoding="utf-8") as file_obj:
            parsed_file = BeautifulSoup(file_obj)

        return parsed_file

    def get_content(self, parsed_file: BeautifulSoup) -> str:
        # Find the first h1 tag (The book title)
        title_h1 = parsed_file.find("h1")

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

    def get_metadata(self, parsed_file: BeautifulSoup, tag_name: str) -> str:
        return parsed_file.find("meta", {"name": tag_name})["content"]