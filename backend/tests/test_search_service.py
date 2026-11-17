
import pytest

from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.services.search_service import SemanticSearchService


@pytest.fixture
def search_setup(tmp_path):
    storage_path = str(tmp_path / "search_test")

    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        storage_path=storage_path,
        collection_name="documind_documents",
        vector_size=384
    )

    documents = [
        {
            "text": "Python is widely used for artificial intelligence and machine learning.",
            "document_filename": "ai_guide.txt",
            "chunk_id": "chunk-1"
        },
        {
            "text": "FastAPI is a modern Python framework for building web APIs.",
            "document_filename": "backend_guide.txt",
            "chunk_id": "chunk-2"
        },
        {
            "text": "Cricket is a popular sport played between two teams.",
            "document_filename": "sports_guide.txt",
            "chunk_id": "chunk-3"
        }
    ]

    texts = [document["text"] for document in documents]
    embeddings = embedding_service.generate_embeddings(texts)

    embedded_chunks = []

    for document, embedding in zip(documents, embeddings):
        embedded_chunks.append({
            **document,
            "embedding": embedding,
            "sources": []
        })

    vector_store.add_documents(embedded_chunks)
    vector_store.close()

    search_service = SemanticSearchService(
        storage_path=storage_path
    )

    yield search_service

    search_service.close()


def test_semantic_search_returns_results(search_setup):
    results = search_setup.search(
        "What programming language is used for AI?",
        limit=3
    )

    assert len(results) > 0
    assert results[0]["text"]


def test_semantic_search_relevant_document(search_setup):
    results = search_setup.search(
        "Which language is useful for machine learning?",
        limit=3
    )

    assert results[0]["document"] == "ai_guide.txt"


def test_search_result_contains_metadata(search_setup):
    results = search_setup.search(
        "How can I build web APIs?",
        limit=3
    )

    assert "document" in results[0]
    assert "text" in results[0]
    assert "score" in results[0]
    assert "sources" in results[0]
    assert "chunk_id" in results[0]


def test_empty_search_query(search_setup):
    with pytest.raises(ValueError):
        search_setup.search("")


def test_invalid_search_query(search_setup):
    with pytest.raises(TypeError):
        search_setup.search(123)


def test_invalid_search_limit(search_setup):
    with pytest.raises(ValueError):
        search_setup.search("Python programming", limit=0)

def test_search_with_document_filter(search_setup):
    results = search_setup.search(
        "Python machine learning",
        limit=5,
        document_filename="ai_guide.txt"
    )

    assert len(results) == 1
    assert results[0]["document"] == "ai_guide.txt"


def test_search_with_nonexistent_document(search_setup):
    results = search_setup.search(
        "Python machine learning",
        document_filename="missing.txt"
    )

    assert results == []
