
import pytest

from backend.app.services.reranking_service import RerankingService


@pytest.fixture(scope="module")
def reranker():
    return RerankingService()


def test_rerank_relevant_documents(reranker):
    query = "Which programming language is used for AI?"

    documents = [
        {
            "chunk_id": "chunk-1",
            "text": "Python is widely used for artificial intelligence and machine learning."
        },
        {
            "chunk_id": "chunk-2",
            "text": "Cricket is a popular sport played between two teams."
        },
        {
            "chunk_id": "chunk-3",
            "text": "Python is a programming language used for software development."
        }
    ]

    results = reranker.rerank(query, documents, top_k=3)

    assert len(results) == 3
    assert results[0]["chunk_id"] in ["chunk-1", "chunk-3"]


def test_rerank_top_k(reranker):
    documents = [
        {"text": "Python is a programming language."},
        {"text": "Cricket is a sport."},
        {"text": "AI uses machine learning."}
    ]

    results = reranker.rerank(
        "Tell me about Python",
        documents,
        top_k=2
    )

    assert len(results) == 2


def test_rerank_score_exists(reranker):
    documents = [
        {"text": "Python is used for machine learning."}
    ]

    results = reranker.rerank(
        "What is Python used for?",
        documents
    )

    assert "rerank_score" in results[0]
    assert isinstance(results[0]["rerank_score"], float)


def test_rerank_descending_order(reranker):
    documents = [
        {"text": "Cricket is played with a bat and ball."},
        {"text": "Python is a programming language."},
        {"text": "Machine learning is a field of AI."}
    ]

    results = reranker.rerank(
        "Explain artificial intelligence and machine learning.",
        documents
    )

    scores = [item["rerank_score"] for item in results]

    assert scores == sorted(scores, reverse=True)


def test_empty_documents(reranker):
    assert reranker.rerank("Python programming", []) == []


def test_empty_query(reranker):
    with pytest.raises(ValueError):
        reranker.rerank("", [{"text": "Python programming"}])


def test_invalid_query(reranker):
    with pytest.raises(TypeError):
        reranker.rerank(123, [{"text": "Python programming"}])


def test_invalid_top_k(reranker):
    with pytest.raises(ValueError):
        reranker.rerank(
            "Python programming",
            [{"text": "Python is a language."}],
            top_k=0
        )


def test_invalid_document_text(reranker):
    with pytest.raises(ValueError):
        reranker.rerank(
            "Python programming",
            [{"text": ""}]
        )
