
from unittest.mock import MagicMock, patch

import pytest

from backend.app.services.rag_service import RAGService


@pytest.fixture
def mock_rag_service():
    with patch(
        "backend.app.services.rag_service.HybridSearchService"
    ) as mock_search, patch(
        "backend.app.services.rag_service.LLMService"
    ) as mock_llm:

        service = RAGService()

        yield service, mock_search.return_value, mock_llm.return_value


def test_answer_question_success(mock_rag_service):
    service, mock_search, mock_llm = mock_rag_service

    mock_search.search.return_value = [
        {
            "rank": 1,
            "chunk_id": "chunk-001",
            "document": "python.pdf",
            "text": "Python was created by Guido van Rossum.",
            "score": 0.95,
            "sources": [{"page": 1}]
        }
    ]

    mock_llm.generate_answer.return_value = (
        "Python was created by Guido van Rossum."
    )

    result = service.answer_question("Who created Python?")

    assert result["question"] == "Who created Python?"
    assert "Guido van Rossum" in result["answer"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["document"] == "python.pdf"

    mock_llm.generate_answer.assert_called_once()


def test_answer_question_no_results(mock_rag_service):
    service, mock_search, mock_llm = mock_rag_service

    mock_search.search.return_value = []

    result = service.answer_question("Who created Python?")

    assert result["sources"] == []
    assert "do not contain enough information" in result["answer"]

    mock_llm.generate_answer.assert_not_called()


def test_answer_question_empty_query(mock_rag_service):
    service, _, _ = mock_rag_service

    with pytest.raises(ValueError):
        service.answer_question("")


def test_answer_question_invalid_query(mock_rag_service):
    service, _, _ = mock_rag_service

    with pytest.raises(TypeError):
        service.answer_question(None)


def test_answer_question_invalid_limit(mock_rag_service):
    service, _, _ = mock_rag_service

    with pytest.raises(ValueError):
        service.answer_question("What is Python?", limit=0)


def test_document_filter_is_passed(mock_rag_service):
    service, mock_search, _ = mock_rag_service

    mock_search.search.return_value = []

    service.answer_question(
        query="What is Python?",
        document_filename="python.pdf"
    )

    mock_search.search.assert_called_once_with(
        query="What is Python?",
        limit=5,
        document_filename="python.pdf"
    )


def test_close_search_service(mock_rag_service):
    service, mock_search, _ = mock_rag_service

    service.close()

    mock_search.close.assert_called_once()

def test_irrelevant_results_are_rejected(mock_rag_service):
    service, mock_search, mock_llm = mock_rag_service

    mock_search.search.return_value = [
        {
            "rank": 1,
            "chunk_id": "chunk-001",
            "document": "sample_rag.txt",
            "text": "Python was created by Guido van Rossum.",
            "score": -11.14,
            "sources": [{"page": 1}]
        }
    ]

    result = service.answer_question(
        "What is the capital of France?"
    )

    assert result["sources"] == []
    assert "do not contain enough information" in result["answer"]

    mock_llm.generate_answer.assert_not_called()
