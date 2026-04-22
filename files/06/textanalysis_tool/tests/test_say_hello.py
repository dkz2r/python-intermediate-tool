import pytest

from textanalysis_tool.say_hello import hello


def test_hello():
    assert hello("My Name") == "Hello, My Name!"


def test_hello_empty_string():
    with pytest.raises(ValueError):
        hello("")
