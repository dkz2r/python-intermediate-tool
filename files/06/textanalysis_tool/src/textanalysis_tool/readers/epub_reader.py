import re

from bs4 import BeautifulSoup
import ebooklib

from textanalysis_tool.readers.base_reader import BaseReader


class EPUBReader(BaseReader):
    SOURCE_URL_PATTERN = "https://www.gutenberg.org/files/([0-9]+)/[0-9]+-h/[0-9]+-h.htm"

    def read(self, filepath: str) -> ebooklib.epub.EpubBook:
        book = ebooklib.epub.read_epub(filepath)
        if not book:
            raise ValueError("The file could not be parsed as EPUB.")
        return book

    def get_content(self, filepath):
        book = self.read(filepath)
        text = ""
        for section in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = section.get_content()
            soup = BeautifulSoup(content, features="html.parser")
            text += soup.get_text()
        return text

    def get_metadata(self, filepath) -> dict:
        book = self.read(filepath)

        source_url = book.get_metadata(namespace="DC", name="source")[0][0]
        extracted_id = re.search(self.SOURCE_URL_PATTERN, source_url, re.DOTALL).group(1)

        metadata = {
            "title": book.get_metadata(namespace="DC", name="title")[0][0],
            "author": book.get_metadata(namespace="DC", name="creator")[0][0],
            "extracted_id": int(extracted_id) if extracted_id else None,
        }
        return metadata
