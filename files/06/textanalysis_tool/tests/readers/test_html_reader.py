import pytest
from unittest.mock import mock_open

from textanalysis_tool.readers.html_reader import HTMLReader

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


def test_get_content():
    reader = HTMLReader()
    content = reader.get_content("dummy_path.html")
    assert "This is a test document." in content
    assert "It is only a test document." in content


def test_get_metadata():
    reader = HTMLReader()
    metadata = reader.get_metadata("dummy_path.html")
    assert metadata["title"] == "Test Document"
    assert metadata["author"] == "Test Author"
    assert metadata["id"] == 1234
