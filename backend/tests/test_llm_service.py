
from unittest.mock import MagicMock, patch

import pytest

from backend.app.services.llm_service import LLMService


def test_generate_answer():
    with patch(
        "backend.app.services.llm_service.ollama.Client"
    ) as mock_client:

        mock_response = MagicMock()
        mock_response.message.content = (
            "Python was created by Guido van Rossum."
        )

        mock_client.return_value.chat.return_value = mock_response

        service = LLMService()

        answer = service.generate_answer(
            query="Who created Python?",
            context="Python was created by Guido van Rossum."
        )

        assert answer == "Python was created by Guido van Rossum."


def test_empty_query():
    service = LLMService()

    with pytest.raises(ValueError):
        service.generate_answer("", "Some document context")


def test_empty_context():
    service = LLMService()

    with pytest.raises(ValueError):
        service.generate_answer("What is Python?", "")


def test_invalid_query_type():
    service = LLMService()

    with pytest.raises(TypeError):
        service.generate_answer(None, "Some context")


def test_invalid_context_type():
    service = LLMService()

    with pytest.raises(TypeError):
        service.generate_answer("What is Python?", None)


def test_empty_response_is_returned():
    with patch(
        "backend.app.services.llm_service.ollama.Client"
    ) as mock_client:

        mock_response = MagicMock()
        mock_response.message.content = "  "

        mock_client.return_value.chat.return_value = mock_response

        service = LLMService()

        answer = service.generate_answer(
            query="What is Python?",
            context="Python is a programming language."
        )

        assert answer == ""
