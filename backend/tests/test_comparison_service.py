
from unittest.mock import patch

import pytest

from backend.app.services.comparison_service import (
    DocumentComparisonService
)


@pytest.fixture
def mock_comparison_service():
    with patch(
        "backend.app.services.comparison_service.LLMService"
    ) as mock_llm:

        service = DocumentComparisonService()
        yield service, mock_llm.return_value


def test_compare_documents(mock_comparison_service):
    service, mock_llm = mock_comparison_service

    mock_llm.generate_answer.return_value = (
        "Both documents discuss Python programming."
    )

    result = service.compare(
        "Python was created in 1991.",
        "Python was released in 1991."
    )

    assert "Both documents discuss Python" in result
    mock_llm.generate_answer.assert_called_once()


def test_empty_document_a(mock_comparison_service):
    service, _ = mock_comparison_service

    with pytest.raises(ValueError):
        service.compare("", "Document B content")


def test_empty_document_b(mock_comparison_service):
    service, _ = mock_comparison_service

    with pytest.raises(ValueError):
        service.compare("Document A content", "")


def test_invalid_document_a_type(mock_comparison_service):
    service, _ = mock_comparison_service

    with pytest.raises(TypeError):
        service.compare(None, "Document B content")


def test_invalid_document_b_type(mock_comparison_service):
    service, _ = mock_comparison_service

    with pytest.raises(TypeError):
        service.compare("Document A content", None)


def test_both_documents_are_sent_to_llm(
    mock_comparison_service
):
    service, mock_llm = mock_comparison_service

    mock_llm.generate_answer.return_value = "Comparison complete."

    service.compare(
        "Python is used in AI.",
        "Python is used in web development."
    )

    call_args = mock_llm.generate_answer.call_args

    context = call_args.kwargs["context"]

    assert "Python is used in AI." in context
    assert "Python is used in web development." in context
