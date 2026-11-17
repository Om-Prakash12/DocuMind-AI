
import fitz
import pytest

from backend.app.services.pdf_parser import extract_pdf


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a temporary PDF for testing."""

    pdf_path = tmp_path / "sample.pdf"

    with fitz.open() as pdf:

        page1 = pdf.new_page()
        page1.insert_text(
            (72, 72),
            "DocuMind is an AI document intelligence platform."
        )

        page2 = pdf.new_page()
        page2.insert_text(
            (72, 72),
            "It uses Python and Retrieval Augmented Generation."
        )

        pdf.save(pdf_path)

    return pdf_path


def test_extract_pdf(sample_pdf):

    result = extract_pdf(str(sample_pdf))

    assert result["filename"] == "sample.pdf"
    assert result["total_pages"] == 2

    assert len(result["pages"]) == 2

    assert result["pages"][0]["page_number"] == 1
    assert result["pages"][1]["page_number"] == 2

    assert "DocuMind" in result["pages"][0]["text"]
    assert "Python" in result["pages"][1]["text"]

    assert result["empty_pages"] == []


def test_pdf_file_not_found():

    with pytest.raises(FileNotFoundError):
        extract_pdf("missing.pdf")


def test_invalid_file_extension(tmp_path):

    text_file = tmp_path / "sample.txt"
    text_file.write_text("This is not a PDF.")

    with pytest.raises(ValueError):
        extract_pdf(str(text_file))
