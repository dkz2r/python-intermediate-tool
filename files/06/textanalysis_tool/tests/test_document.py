import pytest

from textanalysis_tool.document import Document
from textanalysis_tool.readers.base_reader import BaseReader


class MockReader(BaseReader):
    def get_content(self, filepath: str) -> str:
        return "This is a test document. It contains words.\nIt is only a test document."

    def get_metadata(self, filepath: str) -> dict:
        return {
            "title": "Test Document",
            "author": "Test Author",
            "id": 1234,
        }


def test_create_document():
    doc = Document(filepath="dummy_path.txt", reader=MockReader())
    assert doc.title == "Test Document"
    assert doc.author == "Test Author"
    assert isinstance(doc.id, int) and doc.id == 1234


def test_line_count():
    doc = Document(filepath="dummy_path.txt", reader=MockReader())
    assert doc.line_count == 2


def test_get_word_occurrence():
    doc = Document(filepath="dummy_path.txt", reader=MockReader())
    assert doc.get_word_occurrence("test") == 2
