
from pathlib import Path

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table


def extract_docx(file_path: str) -> dict:
    """
    Extract paragraphs, headings and tables from a DOCX document.
    Preserve their original document order.
    """

    path = Path(file_path)

    # 1. Validate the file
    if not path.exists():
        raise FileNotFoundError(f"DOCX file not found: {path}")

    if not path.is_file():
        raise ValueError("The supplied path is not a file.")

    if path.suffix.lower() != ".docx":
        raise ValueError("Only DOCX files are supported.")

    try:
        document = Document(str(path))

        paragraphs = []
        tables = []
        content_blocks = []

        # 2. Process paragraphs and tables in document order
        for element in document.iter_inner_content():

            # 3. Identify Paragraph objects correctly
            if isinstance(element, Paragraph):

                text = element.text.strip()

                if not text:
                    continue

                style_name = (
                    element.style.name
                    if element.style else "Normal"
                )

                paragraph_data = {
                    "paragraph_index": len(paragraphs) + 1,
                    "text": text,
                    "style": style_name,
                    "is_heading": style_name.startswith("Heading")
                }

                paragraphs.append(paragraph_data)

                content_blocks.append({
                    "type": "paragraph",
                    **paragraph_data
                })

            # 4. Identify Table objects correctly
            elif isinstance(element, Table):

                table_rows = []

                for row in element.rows:
                    cells = [
                        cell.text.strip()
                        for cell in row.cells
                    ]

                    table_rows.append(cells)

                if not table_rows:
                    continue

                table_data = {
                    "table_index": len(tables) + 1,
                    "rows": table_rows
                }

                tables.append(table_data)

                content_blocks.append({
                    "type": "table",
                    **table_data
                })

        # 5. Extract document metadata
        properties = document.core_properties

        # 6. Calculate document statistics
        text_parts = []

        for block in content_blocks:

            if block["type"] == "paragraph":
                text_parts.append(block["text"])

            elif block["type"] == "table":
                for row in block["rows"]:
                    text_parts.append(" | ".join(row))

        full_text = "\n".join(text_parts)

        return {
            "filename": path.name,
            "total_paragraphs": len(paragraphs),
            "total_tables": len(tables),
            "total_characters": len(full_text),

            "metadata": {
                "title": properties.title,
                "author": properties.author,
                "subject": properties.subject
            },

            "paragraphs": paragraphs,
            "tables": tables,
            "content_blocks": content_blocks
        }

    except Exception as exc:
        raise ValueError(
            f"Unable to process DOCX: {exc}"
        ) from exc
