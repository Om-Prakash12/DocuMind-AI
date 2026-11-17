
import pytest

from backend.app.services.storage_pipeline import (
    DocumentStoragePipeline
)


@pytest.fixture
def storage_pipeline(tmp_path):
    pipeline = DocumentStoragePipeline(
        storage_path=str(tmp_path / "qdrant_storage")
    )

    yield pipeline
    pipeline.close()


def test_complete_document_storage(storage_pipeline, tmp_path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "DocuMind is an AI document intelligence platform. "
        "It uses Python and FastAPI for backend development. "
        "Machine learning enables semantic document search. "
        "Qdrant stores document embeddings for retrieval.",
        encoding="utf-8"
    )

    result = storage_pipeline.ingest(
        str(file_path),
        chunk_size=10,
        chunk_overlap=2
    )

    assert result["status"] == "success"
    assert result["filename"] == "sample.txt"
    assert result["file_type"] == "txt"
    assert result["total_chunks"] > 0
    assert result["stored_vectors"] == result["total_chunks"]
    assert result["embedding_dimension"] == 384


def test_empty_document_storage(storage_pipeline, tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    result = storage_pipeline.ingest(str(file_path))

    assert result["status"] == "success"
    assert result["total_chunks"] == 0
    assert result["stored_vectors"] == 0


def test_qdrant_count_after_ingestion(storage_pipeline, tmp_path):
    file_path = tmp_path / "count_test.txt"

    file_path.write_text(
        "Python is useful for artificial intelligence. "
        "FastAPI helps developers build APIs.",
        encoding="utf-8"
    )

    result = storage_pipeline.ingest(
        str(file_path),
        chunk_size=5,
        chunk_overlap=1
    )

    stored_count = storage_pipeline.vector_store.count_documents()

    assert stored_count == result["stored_vectors"]
    assert stored_count > 0
