import pytest
from unittest.mock import mock_open

from textanalysis_tool.document import Document


@pytest.fixture(autouse=True)
def mock_file(monkeypatch):
    mock = mock_open(
        read_data="This is a test document. It contains words.\nIt is only a test document."
    )
    monkeypatch.setattr("builtins.open", mock)
    return mock


@pytest.fixture
def doc():
    Document.CONTENT_PATTERN = r"(.*)"
    return Document(filepath="tests/example_file.txt")


def test_create_document(doc):
    assert doc.filepath == "tests/example_file.txt"


def test_document_word_count(doc):
    assert doc.get_line_count() == 2


def test_document_word_occurrence(doc):
    assert doc.get_word_occurrence("test") == 2


def test_empty_file(monkeypatch):
    # Mock an empty file
    mock = mock_open(read_data="")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        Document(filepath="empty_file.txt")


def test_binary_file(monkeypatch):
    # Mock a binary file
    mock = mock_open(read_data=b"\x00\x01\x02")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        Document(filepath="binary_file.bin")
