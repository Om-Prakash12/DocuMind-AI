
from pathlib import Path


def extract_txt(file_path: str) -> dict:
    """
    Extract text and line-level information from a TXT file.
    """

    path = Path(file_path)

    # 1. Validate the file
    if not path.exists():
        raise FileNotFoundError(f"TXT file not found: {path}")

    if not path.is_file():
        raise ValueError("The supplied path is not a file.")

    if path.suffix.lower() != ".txt":
        raise ValueError("Only TXT files are supported.")

    try:
        # 2. Read the file
        text = path.read_text(
            encoding="utf-8-sig",
            errors="replace"
        )

        # 3. Extract individual lines
        lines = []

        for line_number, line in enumerate(
            text.splitlines(), start=1
        ):
            cleaned_line = line.strip()

            if cleaned_line:
                lines.append({
                    "line_number": line_number,
                    "text": cleaned_line
                })

        # 4. Return structured document data
        return {
            "filename": path.name,
            "total_lines": len(text.splitlines()),
            "non_empty_lines": len(lines),
            "total_characters": len(text),
            "text": text,
            "lines": lines
        }

    except OSError as exc:
        raise ValueError(
            f"Unable to read TXT file: {exc}"
        ) from exc
