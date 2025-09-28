import pytest
from unittest.mock import mock_open

from textanalysis_tool.plain_text_document import PlainTextDocument

TEST_DATA = """
Title: Test Document

Author: Test Author

Release date: January 1, 2001 [eBook #1234]
                Most recently updated: February 2, 2002

*** START OF THE PROJECT GUTENBERG EBOOK TEST ***
This is a test document. It contains words.
It is only a test document.
*** END OF THE PROJECT GUTENBERG EBOOK TEST ***
"""


@pytest.fixture(autouse=True)
def mock_file(monkeypatch):
    mock = mock_open(read_data=TEST_DATA)
    monkeypatch.setattr("builtins.open", mock)
    return mock


@pytest.fixture
def doc():
    return PlainTextDocument(filepath="tests/example_file.txt")


def test_create_document(doc):
    assert doc.title == "Test Document"
    assert doc.author == "Test Author"
    assert isinstance(doc.id, int) and doc.id == 1234


def test_empty_file(monkeypatch):
    # Mock an empty file
    mock = mock_open(read_data="")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        PlainTextDocument(filepath="empty_file.txt")


def test_binary_file(monkeypatch):
    # Mock a binary file
    mock = mock_open(read_data=b"\x00\x01\x02")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        PlainTextDocument(filepath="binary_file.bin")


def test_document_line_count(doc):
    assert doc.line_count == 2


def test_document_word_occurrence(doc):
    assert doc.get_word_occurrence("test") == 2
