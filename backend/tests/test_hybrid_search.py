
import pytest

from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.services.hybrid_search import HybridSearchService


@pytest.fixture
def hybrid_setup(tmp_path):
    storage_path = str(tmp_path / "hybrid_test")

    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        storage_path=storage_path,
        collection_name="documind_documents",
        vector_size=384
    )

    documents = [
        {
            "chunk_id": "chunk-1",
            "text": "Python is widely used for artificial intelligence and machine learning.",
            "document_filename": "ai_guide.txt",
            "document_type": "txt",
            "sources": []
        },
        {
            "chunk_id": "chunk-2",
            "text": "FastAPI is a modern Python framework for building web APIs.",
            "document_filename": "backend_guide.txt",
            "document_type": "txt",
            "sources": []
        },
        {
            "chunk_id": "chunk-3",
            "text": "Cricket is a popular sport played between two teams.",
            "document_filename": "sports_guide.txt",
            "document_type": "txt",
            "sources": []
        }
    ]

    embeddings = embedding_service.generate_embeddings(
        [document["text"] for document in documents]
    )

    embedded_chunks = [
        {**document, "embedding": embedding}
        for document, embedding in zip(documents, embeddings)
    ]

    vector_store.add_documents(embedded_chunks)
    vector_store.close()

    service = HybridSearchService(storage_path=storage_path)

    yield service

    service.close()


def test_hybrid_search_returns_results(hybrid_setup):
    results = hybrid_setup.search(
        "What programming language is used for AI?",
        limit=3
    )

    assert len(results) > 0
    assert results[0]["text"]


def test_hybrid_search_relevant_document(hybrid_setup):
    results = hybrid_setup.search(
        "Python artificial intelligence machine learning",
        limit=3
    )

    assert results[0]["document"] == "ai_guide.txt"


def test_hybrid_search_result_metadata(hybrid_setup):
    results = hybrid_setup.search(
        "How to build web APIs?",
        limit=3
    )

    assert "rank" in results[0]
    assert "chunk_id" in results[0]
    assert "document" in results[0]
    assert "text" in results[0]
    assert "score" in results[0]
    assert "sources" in results[0]


def test_hybrid_search_document_filter(hybrid_setup):
    results = hybrid_setup.search(
        "Python programming",
        limit=5,
        document_filename="backend_guide.txt"
    )

    assert all(
        result["document"] == "backend_guide.txt"
        for result in results
    )


def test_hybrid_search_missing_document(hybrid_setup):
    results = hybrid_setup.search(
        "Python programming",
        document_filename="missing.txt"
    )

    assert results == []


def test_hybrid_search_empty_query(hybrid_setup):
    with pytest.raises(ValueError):
        hybrid_setup.search("")


def test_hybrid_search_invalid_query(hybrid_setup):
    with pytest.raises(TypeError):
        hybrid_setup.search(123)


def test_hybrid_search_invalid_limit(hybrid_setup):
    with pytest.raises(ValueError):
        hybrid_setup.search("Python", limit=0)
