import pytest
from unittest.mock import mock_open

from textanalysis_tool.html_document import HTMLDocument

TEST_DATA = """
<head>
  <meta name="dc.title" content="Test Document">
  <meta name="dcterms.source" content="https://www.gutenberg.org/files/1234/1234-h/1234-h.htm">
  <meta name="dc.creator" content="Test Author">
</head>
<body>
  <h1>Test Document</h1>
  <p>
    This is a test document. It contains words.
    It is only a test document.
  </p>
</body>
"""


@pytest.fixture(autouse=True)
def mock_file(monkeypatch):
    mock = mock_open(read_data=TEST_DATA)
    monkeypatch.setattr("builtins.open", mock)
    return mock


@pytest.fixture
def doc():
    return HTMLDocument(filepath="tests/example_file.txt")


def test_create_document(doc):
    assert doc.title == "Test Document"
    assert doc.author == "Test Author"
    assert isinstance(doc.id, int) and doc.id == 1234


def test_empty_file(monkeypatch):
    # Mock an empty file
    mock = mock_open(read_data="")
    monkeypatch.setattr("builtins.open", mock)

    with pytest.raises(ValueError):
        HTMLDocument(filepath="empty_file.html")


def test_document_line_count(doc):
    assert doc.line_count == 2


def test_document_word_occurrence(doc):
    assert doc.get_word_occurrence("test") == 2
