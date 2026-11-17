
import pytest

from backend.app.services.text_cleaner import clean_text


def test_remove_extra_spaces():
    result = clean_text("Hello     DocuMind")
    assert result == "Hello DocuMind"


def test_preserve_paragraphs():
    result = clean_text("First paragraph.\n\nSecond paragraph.")
    assert result == "First paragraph.\n\nSecond paragraph."


def test_remove_excessive_blank_lines():
    result = clean_text("First paragraph.\n\n\n\nSecond paragraph.")
    assert result == "First paragraph.\n\nSecond paragraph."


def test_remove_null_bytes():
    result = clean_text("DocuMind\x00 AI")
    assert result == "DocuMind AI"


def test_empty_text():
    assert clean_text("") == ""


def test_whitespace_only_text():
    assert clean_text("   \n   ") == ""


def test_invalid_input():
    with pytest.raises(TypeError):
        clean_text(123)
