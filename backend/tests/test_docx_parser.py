
from docx import Document
import pytest

from backend.app.services.docx_parser import extract_docx


@pytest.fixture
def sample_docx(tmp_path):
    """Create a sample Word document for testing."""

    docx_path = tmp_path / "sample.docx"

    document = Document()

    document.add_heading("DocuMind Introduction", level=1)

    document.add_paragraph(
        "DocuMind is an AI document intelligence platform."
    )

    table = document.add_table(rows=2, cols=2)

    table.cell(0, 0).text = "Technology"
    table.cell(0, 1).text = "Purpose"

    table.cell(1, 0).text = "Python"
    table.cell(1, 1).text = "Backend Development"

    document.add_paragraph(
        "DocuMind uses AI to analyze documents."
    )

    document.save(docx_path)

    return docx_path


def test_extract_docx(sample_docx):

    result = extract_docx(str(sample_docx))

    assert result["filename"] == "sample.docx"

    assert result["total_paragraphs"] == 3
    assert result["total_tables"] == 1

    assert "DocuMind Introduction" in (
        result["paragraphs"][0]["text"]
    )

    assert result["paragraphs"][0]["is_heading"] is True

    assert result["tables"][0]["rows"][1][0] == "Python"

    assert result["content_blocks"][0]["type"] == "paragraph"
    assert result["content_blocks"][2]["type"] == "table"


def test_docx_file_not_found():

    with pytest.raises(FileNotFoundError):
        extract_docx("missing.docx")


def test_invalid_file_extension(tmp_path):

    text_file = tmp_path / "sample.txt"
    text_file.write_text("This is not a Word document.")

    with pytest.raises(ValueError):
        extract_docx(str(text_file))
