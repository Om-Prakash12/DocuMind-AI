
import pytest
from docx import Document

from backend.app.services.ingestion import ingest_document


def test_ingest_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello DocuMind\nAI Document Platform")

    result = ingest_document(str(file_path))

    assert result["file_type"] == "txt"
    assert "Hello DocuMind" in result["text"]
    assert result["statistics"]["total_content_blocks"] == 2


def test_ingest_docx(tmp_path):
    file_path = tmp_path / "sample.docx"

    document = Document()
    document.add_paragraph("DocuMind AI")
    document.add_paragraph("Document Intelligence")
    document.save(file_path)

    result = ingest_document(str(file_path))

    assert result["file_type"] == "docx"
    assert "DocuMind AI" in result["text"]
    assert result["statistics"]["total_paragraphs"] == 2


def test_ingest_pdf(tmp_path):
    import pymupdf

    file_path = tmp_path / "sample.pdf"

    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "DocuMind PDF Test")
    document.save(file_path)
    document.close()

    result = ingest_document(str(file_path))

    assert result["file_type"] == "pdf"
    assert "DocuMind PDF Test" in result["text"]


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "sample.xlsx"
    file_path.write_text("Unsupported format")

    with pytest.raises(ValueError):
        ingest_document(str(file_path))


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        ingest_document("missing_document.txt")
