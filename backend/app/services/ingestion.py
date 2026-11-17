
from pathlib import Path

from backend.app.services.pdf_parser import extract_pdf
from backend.app.services.docx_parser import extract_docx
from backend.app.services.txt_parser import extract_txt


def ingest_document(file_path: str) -> dict:
    """
    Detect the document type, extract its content,
    and return a standardized document structure.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError("The supplied path is not a file.")

    extension = path.suffix.lower()

    # Step 1: Select the appropriate parser
    if extension == ".pdf":
        result = extract_pdf(str(path))
        file_type = "pdf"

        content_blocks = [
            {
                "type": "page",
                "source": {"page_number": page.get("page_number", index + 1)},
                "text": page.get("text", "")
            }
            for index, page in enumerate(result.get("pages", []))
        ]

        full_text = "\n".join(
            block["text"] for block in content_blocks
        )

    elif extension == ".docx":
        result = extract_docx(str(path))
        file_type = "docx"

        content_blocks = []

        for block in result.get("content_blocks", []):
            if block["type"] == "paragraph":
                content_blocks.append({
                    "type": "paragraph",
                    "source": {
                        "paragraph_index": block["paragraph_index"],
                        "style": block["style"]
                    },
                    "text": block["text"]
                })

            elif block["type"] == "table":
                content_blocks.append({
                    "type": "table",
                    "source": {
                        "table_index": block["table_index"]
                    },
                    "rows": block["rows"],
                    "text": "\n".join(
                        " | ".join(row) for row in block["rows"]
                    )
                })

        full_text = "\n".join(
            block["text"] for block in content_blocks
        )

    elif extension == ".txt":
        result = extract_txt(str(path))
        file_type = "txt"

        content_blocks = [
            {
                "type": "line",
                "source": {"line_number": line["line_number"]},
                "text": line["text"]
            }
            for line in result.get("lines", [])
        ]

        full_text = result.get("text", "")

    else:
        raise ValueError(
            "Unsupported file format. Use PDF, DOCX, or TXT."
        )

    # Step 2: Return a standardized structure
    return {
        "filename": path.name,
        "file_type": file_type,
        "total_characters": len(full_text),
        "text": full_text,
        "content_blocks": content_blocks,
        "metadata": result.get("metadata", {}),
        "statistics": {
            "total_content_blocks": len(content_blocks),
            "total_pages": result.get("total_pages", 0),
            "total_paragraphs": result.get("total_paragraphs", 0),
            "total_tables": result.get("total_tables", 0),
            "total_lines": result.get("total_lines", 0)
        }
    }
