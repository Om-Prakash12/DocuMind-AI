
import pytest

from backend.app.services.txt_parser import extract_txt


@pytest.fixture
def sample_txt(tmp_path):

    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "DocuMind AI\n"
        "Document Intelligence Platform\n"
        "\n"
        "Built using Python and FastAPI.\n",
        encoding="utf-8"
    )

    return file_path


def test_extract_txt(sample_txt):

    result = extract_txt(str(sample_txt))

    assert result["filename"] == "sample.txt"
    assert result["total_lines"] == 4
    assert result["non_empty_lines"] == 3

    assert "DocuMind AI" in result["text"]

    assert result["lines"][0]["line_number"] == 1
    assert result["lines"][0]["text"] == "DocuMind AI"

    assert result["lines"][2]["line_number"] == 4


def test_txt_file_not_found():

    with pytest.raises(FileNotFoundError):
        extract_txt("missing.txt")


def test_invalid_file_extension(tmp_path):

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_text("Not a TXT document.")

    with pytest.raises(ValueError):
        extract_txt(str(pdf_file))
