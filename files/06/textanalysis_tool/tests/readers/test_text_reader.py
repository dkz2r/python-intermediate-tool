import pytest
from unittest.mock import mock_open

from textanalysis_tool.readers.text_reader import TextReader

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


def test_get_content():
    reader = TextReader()
    content = reader.get_content("dummy_path.txt")
    assert "This is a test document." in content
    assert "It is only a test document." in content


def test_get_metadata():
    reader = TextReader()
    metadata = reader.get_metadata("dummy_path.txt")
    assert metadata["title"] == "Test Document"
    assert metadata["author"] == "Test Author"
    assert metadata["id"] == 1234
