
import pytest

from backend.app.services.chunker import chunk_content_blocks


def test_preserve_pdf_page_source():
    blocks = [
        {
            "type": "page",
            "source": {"page_number": 1},
            "text": "DocuMind document intelligence"
        },
        {
            "type": "page",
            "source": {"page_number": 2},
            "text": "Artificial intelligence platform"
        }
    ]

    result = chunk_content_blocks(blocks, chunk_size=3, chunk_overlap=0)

    assert result[0]["sources"][0]["page_number"] == 1
    assert result[1]["sources"][0]["page_number"] == 2


def test_preserve_docx_paragraph_source():
    blocks = [
        {
            "type": "paragraph",
            "source": {"paragraph_index": 1},
            "text": "First paragraph"
        },
        {
            "type": "paragraph",
            "source": {"paragraph_index": 2},
            "text": "Second paragraph"
        }
    ]

    result = chunk_content_blocks(blocks, chunk_size=2, chunk_overlap=0)

    assert result[0]["sources"][0]["paragraph_index"] == 1
    assert result[1]["sources"][0]["paragraph_index"] == 2


def test_chunk_spanning_multiple_sources():
    blocks = [
        {
            "type": "page",
            "source": {"page_number": 1},
            "text": "one two three"
        },
        {
            "type": "page",
            "source": {"page_number": 2},
            "text": "four five six"
        }
    ]

    result = chunk_content_blocks(
        blocks,
        chunk_size=4,
        chunk_overlap=0
    )

    assert len(result[0]["sources"]) == 2
    assert result[0]["sources"][0]["page_number"] == 1
    assert result[0]["sources"][1]["page_number"] == 2


def test_empty_content_blocks():
    assert chunk_content_blocks([]) == []


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_content_blocks([], chunk_size=0)
