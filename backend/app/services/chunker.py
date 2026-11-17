
from uuid import uuid4


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[dict]:
    """
    Split text into overlapping word-based chunks.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0
    chunk_index = 1

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]

        chunk = {
            "chunk_id": str(uuid4()),
            "chunk_index": chunk_index,
            "text": " ".join(chunk_words),
            "word_count": len(chunk_words),
            "start_word": start,
            "end_word": end
        }

        chunks.append(chunk)

        if end == len(words):
            break

        start = end - chunk_overlap
        chunk_index += 1

    return chunks

def chunk_content_blocks(
    content_blocks: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[dict]:
    """
    Create overlapping chunks while preserving original
    document source locations.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    # Flatten words while retaining their source information
    words = []

    for block_index, block in enumerate(content_blocks):
        text = block.get("text", "")

        if not isinstance(text, str):
            raise TypeError("Every content block must contain text.")

        block_words = text.split()

        for word_index, word in enumerate(block_words):
            words.append({
                "word": word,
                "source": block.get("source", {}),
                "block_type": block.get("type", "unknown"),
                "block_index": block_index,
                "word_index": word_index
            })

    if not words:
        return []

    chunks = []
    start = 0
    chunk_index = 1

    while start < len(words):
        end = min(start + chunk_size, len(words))
        selected_words = words[start:end]

        # Collect unique source locations used by this chunk
        sources = []
        seen_sources = set()

        for item in selected_words:
            source_key = (
                item["block_index"],
                item["block_type"]
            )

            if source_key not in seen_sources:
                seen_sources.add(source_key)

                sources.append({
                    "block_type": item["block_type"],
                    "block_index": item["block_index"],
                    **item["source"]
                })

        chunks.append({
            "chunk_id": str(uuid4()),
            "chunk_index": chunk_index,
            "text": " ".join(
                item["word"] for item in selected_words
            ),
            "word_count": len(selected_words),
            "start_word": start,
            "end_word": end,
            "sources": sources
        })

        if end == len(words):
            break

        start = end - chunk_overlap
        chunk_index += 1

    return chunks
