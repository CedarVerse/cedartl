from abc import abstractmethod
from io import TextIOWrapper, FileIO, BufferedRandom, BufferedWriter, BufferedReader

import pytest
from importlib.resources.abc import Traversable
from typing import Dict, overload, BinaryIO, IO, Any

from cedartl import CedarTLProcessor


class MockTraversable(Traversable):
    """Mock implementation of Traversable for testing"""

    def __init__(self, files: Dict[str, str]):
        self.files = files

    def __truediv__(self, other: str) -> 'MockTraversable':
        self.other = other
        return self

    def read_text(self, encoding: str | None = None) -> str:
        filename = str(self).split('/')[-1]
        template_name = filename.replace('.cedartl', '')
        if template_name not in self.files:
            raise OSError(f"File not found: {filename}")
        return self.files[template_name]

    def __str__(self) -> str:
        return f"mock/path/{self.other}.cedartl"

    def is_dir(self):
        return self.other is None

    def is_file(self):
        return self.other is not None

    def iterdir(self):
        raise ValueError()

    @overload
    @abstractmethod
    def open(
        self,
        mode="r",
        buffering: int = ...,
        encoding: str | None = ...,
        errors: str | None = ...,
        newline: str | None = ...,
    ) -> TextIOWrapper: ...

    @overload
    @abstractmethod
    def open(
        self, mode, buffering, encoding: None = None, errors: None = None, newline: None = None
    ) -> FileIO: ...

    @overload
    @abstractmethod
    def open(
        self,
        mode,
        buffering = ...,
        encoding: None = None,
        errors: None = None,
        newline: None = None,
    ) -> BufferedRandom: ...

    @overload
    @abstractmethod
    def open(
        self,
        mode,
        buffering = ...,
        encoding: None = None,
        errors: None = None,
        newline: None = None,
    ) -> BufferedWriter: ...

    @overload
    @abstractmethod
    def open(
        self,
        mode,
        buffering = ...,
        encoding: None = None,
        errors: None = None,
        newline: None = None,
    ) -> BufferedReader: ...

    @overload
    @abstractmethod
    def open(
        self, mode, buffering: int = ..., encoding: None = None, errors: None = None, newline: None = None
    ) -> BinaryIO: ...

    @overload
    @abstractmethod
    def open(
        self, mode: str, buffering: int = ..., encoding: str | None = ..., errors: str | None = ..., newline: str | None = ...
    ) -> IO[Any]: ...

    def open(self, mode="r", buffering=..., encoding=..., errors=..., newline=...):
        pass

    @property
    def name(self):
        return self.other

    def read_bytes(self):
        pass


@pytest.fixture
def template_files():
    return {
        "header": r"Welcome \user!",
        "user": "John",
        "user-0": "John Zero",
        "footer": r"Goodbye \user!",
        "nested": r"Start \header End",
        "recursive": r"\recursive",
    }


@pytest.fixture
def processor(template_files):
    mock_folder = MockTraversable(template_files)
    return CedarTLProcessor(mock_folder, MockTraversable({}))


def test_process_simple_template(processor):
    """Test processing a simple template with one replacement"""
    result = processor.process(r"Hello \user!")
    assert result == "Hello John!"


def test_process_empty_input(processor):
    """Test processing empty or None input"""
    assert processor.process("") == ""
    assert processor.process(None) is None


def test_process_no_templates(processor):
    """Test processing text without any templates"""
    text = "Hello World!"
    assert processor.process(text) == text


def test_process_nested_templates(processor):
    """Test processing nested templates"""
    result = processor.process(r"\nested")
    assert result == "Start Welcome John! End"


def test_process_multiple_templates(processor):
    """Test processing multiple templates in one text"""
    result = processor.process(r"\header AB\footer")
    assert result == "Welcome John! ABGoodbye John!"


def test_process_nonexistent_template(processor):
    """Test processing with non-existent template"""
    result = processor.process(r"Hello AB\nonexistent!")
    assert result == r"Hello AB\nonexistent!"


def test_process_recursive_template(processor):
    """Test handling of recursive templates"""
    result = processor.process(r"AB\recursive.")
    assert result == r"AB\recursive."  # Should prevent infinite recursion


def test_invalid_template_name(processor):
    """Test processing with invalid template names"""
    result = processor.process(r"\!invalid")
    assert result == r"\!invalid"


@pytest.mark.parametrize("template_text,expected", [
    (r"\user", "John"),
    (r"\user-", "John-"),
    (r"\user-1", r"\user-1"),
    (r"\user-0", "John Zero"),
    (r"\1user", r"\1user"),
    (r"\.user", r"\.user"),
    (r"\n", r"\n"),
    (r"Hello \user!", "Hello John!"),
    (r"\header \footer", "Welcome John! Goodbye John!"),
    (r"\nonexistent", r"\nonexistent"),
    ("", ""),
    (" ", " "),
    (r"\ ", r"\ "),
])
def test_process_parametrized(processor, template_text, expected):
    """Parametrized test for various template scenarios"""
    assert processor.process(template_text) == expected
