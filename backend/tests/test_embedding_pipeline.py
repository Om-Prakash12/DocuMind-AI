
from backend.app.services.embedding_pipeline import (
    DocumentEmbeddingPipeline
)


def test_complete_document_embedding_pipeline(tmp_path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "DocuMind is an AI document intelligence platform. "
        "It uses Python, FastAPI and machine learning. "
        "Semantic embeddings help retrieve relevant information. "
        "Documents are divided into smaller chunks for processing.",
        encoding="utf-8"
    )

    pipeline = DocumentEmbeddingPipeline()

    result = pipeline.process(
        str(file_path),
        chunk_size=10,
        chunk_overlap=2
    )

    assert result["filename"] == "sample.txt"
    assert result["file_type"] == "txt"
    assert result["total_chunks"] > 0
    assert result["embedding_dimension"] == 384
    assert len(result["embedded_chunks"]) == result["total_chunks"]

    for chunk in result["embedded_chunks"]:
        assert len(chunk["embedding"]) == 384
        assert chunk["word_count"] > 0
        assert chunk["chunk_id"]
        assert chunk["document_filename"] == "sample.txt"


def test_empty_document_embedding_pipeline(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    pipeline = DocumentEmbeddingPipeline()
    result = pipeline.process(str(file_path))

    assert result["total_chunks"] == 0
    assert result["embedded_chunks"] == []
    assert result["embedding_dimension"] == 384
