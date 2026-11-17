
from backend.app.services.ingestion import ingest_document
from backend.app.services.text_cleaner import clean_text
from backend.app.services.chunker import chunk_content_blocks


def process_document(
    file_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> dict:
    """
    Extract, clean and chunk a document while preserving
    original source locations.
    """

    # Step 1: Extract document content
    document = ingest_document(file_path)

    # Step 2: Clean individual content blocks
    cleaned_blocks = []

    for block in document["content_blocks"]:
        cleaned_block = block.copy()

        if "text" in cleaned_block:
            cleaned_block["text"] = clean_text(
                cleaned_block["text"]
            )

        if cleaned_block.get("text"):
            cleaned_blocks.append(cleaned_block)

    # Step 3: Generate source-aware chunks
    chunks = chunk_content_blocks(
        cleaned_blocks,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Step 4: Attach document metadata
    for chunk in chunks:
        chunk["document_filename"] = document["filename"]
        chunk["document_type"] = document["file_type"]

    # Step 5: Combine cleaned text
    cleaned_text = "\n".join(
        block["text"] for block in cleaned_blocks
    )

    # Step 6: Return processed document
    return {
        "filename": document["filename"],
        "file_type": document["file_type"],
        "original_characters": document["total_characters"],
        "cleaned_characters": len(cleaned_text),
        "total_chunks": len(chunks),
        "cleaned_text": cleaned_text,
        "chunks": chunks,
        "metadata": document["metadata"]
    }
