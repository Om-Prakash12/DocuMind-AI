
import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Normalize extracted document text while preserving
    meaningful paragraph boundaries.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text.strip():
        return ""

    # 1. Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # 2. Remove null bytes and unwanted control characters
    text = "".join(
        char
        for char in text
        if char == "\n" or char == "\t"
        or not unicodedata.category(char).startswith("C")
    )

    # 3. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 4. Remove spaces and tabs around line breaks
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)

    # 5. Replace repeated spaces and tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # 6. Limit excessive blank lines to two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 7. Remove leading and trailing whitespace
    return text.strip()
