
from pathlib import Path
import fitz  # PyMuPDF


def extract_pdf(file_path: str) -> dict:
    """
    Extract text and metadata from a PDF document.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Dictionary containing document metadata and page-wise text.
    """

    path = Path(file_path)

    # 1. Validate the file
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.is_file():
        raise ValueError("The supplied path is not a file.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    pages = []

    # 2. Open and process the PDF
    try:
        with fitz.open(path) as pdf:

            if pdf.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported yet."
                )

            # 3. Extract document metadata
            metadata = pdf.metadata or {}

            # 4. Extract text from each page
            for page_index, page in enumerate(pdf):

                text = page.get_text("text", sort=True).strip()

                pages.append({
                    "page_number": page_index + 1,
                    "text": text,
                    "character_count": len(text),
                    "is_empty": not bool(text)
                })

            # 5. Calculate document statistics
            full_text = "\n".join(
                page["text"] for page in pages
            )

            result = {
                "filename": path.name,
                "total_pages": len(pdf),
                "total_characters": len(full_text),
                "metadata": {
                    "title": metadata.get("title"),
                    "author": metadata.get("author"),
                    "subject": metadata.get("subject"),
                    "creator": metadata.get("creator")
                },
                "pages": pages,
                "empty_pages": [
                    page["page_number"]
                    for page in pages
                    if page["is_empty"]
                ]
            }

            return result

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(
            f"Unable to process PDF: {exc}"
        ) from exc
