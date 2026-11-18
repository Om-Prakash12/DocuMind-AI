
from unittest.mock import patch

import pytest

from backend.app.services.summarization_service import (
    SummarizationService
)


@pytest.fixture
def mock_summarization_service():
    with patch(
        "backend.app.services.summarization_service.LLMService"
    ) as mock_llm:

        service = SummarizationService()
        yield service, mock_llm.return_value


def test_short_summary(mock_summarization_service):
    service, mock_llm = mock_summarization_service

    mock_llm.generate_answer.return_value = (
        "Python is a popular programming language."
    )

    result = service.summarize(
        "Python is a popular programming language.",
        summary_type="short"
    )

    assert result == "Python is a popular programming language."
    mock_llm.generate_answer.assert_called_once()


def test_detailed_summary(mock_summarization_service):
    service, mock_llm = mock_summarization_service

    mock_llm.generate_answer.return_value = (
        "Detailed document summary."
    )

    result = service.summarize(
        "Document content about artificial intelligence.",
        summary_type="detailed"
    )

    assert result == "Detailed document summary."


def test_empty_document(mock_summarization_service):
    service, _ = mock_summarization_service

    with pytest.raises(ValueError):
        service.summarize("")


def test_invalid_document_type(mock_summarization_service):
    service, _ = mock_summarization_service

    with pytest.raises(TypeError):
        service.summarize(None)


def test_invalid_summary_type(mock_summarization_service):
    service, _ = mock_summarization_service

    with pytest.raises(ValueError):
        service.summarize(
            "Some document content.",
            summary_type="medium"
        )


def test_llm_called_with_document_context(
    mock_summarization_service
):
    service, mock_llm = mock_summarization_service

    mock_llm.generate_answer.return_value = "Summary."

    service.summarize(
        "Artificial Intelligence is a field of computer science.",
        summary_type="short"
    )

    args = mock_llm.generate_answer.call_args

    assert "Artificial Intelligence" in args.kwargs["context"]
