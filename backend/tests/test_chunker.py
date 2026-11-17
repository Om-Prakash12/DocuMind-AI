
import pytest

from backend.app.services.chunker import chunk_text


def test_empty_text():
    assert chunk_text("") == []


def test_single_chunk():
    result = chunk_text("This is a small document.")

    assert len(result) == 1
    assert result[0]["word_count"] == 5


def test_multiple_chunks():
    text = " ".join(f"word{i}" for i in range(1200))

    result = chunk_text(
        text,
        chunk_size=500,
        chunk_overlap=100
    )

    assert len(result) == 3
    assert result[0]["word_count"] == 500
    assert result[1]["word_count"] == 500
    assert result[2]["word_count"] == 400


def test_chunk_overlap():
    text = " ".join(f"word{i}" for i in range(1000))

    result = chunk_text(
        text,
        chunk_size=500,
        chunk_overlap=100
    )

    first_words = result[0]["text"].split()
    second_words = result[1]["text"].split()

    assert first_words[-100:] == second_words[:100]


def test_chunk_metadata():
    result = chunk_text("One two three four")

    assert result[0]["chunk_index"] == 1
    assert result[0]["start_word"] == 0
    assert result[0]["end_word"] == 4
    assert result[0]["chunk_id"]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("Hello world", chunk_size=0)


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("Hello world", chunk_size=100, chunk_overlap=100)


def test_invalid_input():
    with pytest.raises(TypeError):
        chunk_text(123)


def test_negative_overlap():
    with pytest.raises(ValueError):
        chunk_text("Hello world", chunk_overlap=-1)
