
from docx import Document

from backend.app.services.document_processor import process_document


def test_process_txt_document(tmp_path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "   DocuMind AI    \n\n"
        "Document Intelligence Platform.\n",
        encoding="utf-8"
    )

    result = process_document(
        str(file_path),
        chunk_size=5,
        chunk_overlap=1
    )

    assert result["filename"] == "sample.txt"
    assert result["file_type"] == "txt"
    assert result["total_chunks"] > 0
    assert "DocuMind AI" in result["cleaned_text"]

    for chunk in result["chunks"]:
        assert chunk["document_filename"] == "sample.txt"
        assert chunk["document_type"] == "txt"


def test_process_docx_document(tmp_path):
    file_path = tmp_path / "sample.docx"

    document = Document()
    document.add_paragraph("DocuMind AI Platform")
    document.add_paragraph("Built using Python and FastAPI.")
    document.save(file_path)

    result = process_document(str(file_path))

    assert result["file_type"] == "docx"
    assert result["total_chunks"] >= 1
    assert "DocuMind AI Platform" in result["cleaned_text"]
