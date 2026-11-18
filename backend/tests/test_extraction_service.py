
from unittest.mock import patch

import pytest

from backend.app.services.extraction_service import (
    InformationExtractionService
)


@pytest.fixture
def mock_extraction_service():
    with patch(
        "backend.app.services.extraction_service.LLMService"
    ) as mock_llm:

        service = InformationExtractionService()
        yield service, mock_llm.return_value


def test_successful_extraction(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = (
        '{"creator": "Guido van Rossum", "release_year": 1991}'
    )

    result = service.extract(
        "Python was created by Guido van Rossum in 1991.",
        ["creator", "release_year"]
    )

    assert result["creator"] == "Guido van Rossum"
    assert result["release_year"] == 1991


def test_empty_document(mock_extraction_service):
    service, _ = mock_extraction_service

    with pytest.raises(ValueError):
        service.extract("", ["creator"])


def test_invalid_document_type(mock_extraction_service):
    service, _ = mock_extraction_service

    with pytest.raises(TypeError):
        service.extract(None, ["creator"])


def test_invalid_fields_type(mock_extraction_service):
    service, _ = mock_extraction_service

    with pytest.raises(TypeError):
        service.extract("Python document", "creator")


def test_empty_fields(mock_extraction_service):
    service, _ = mock_extraction_service

    with pytest.raises(ValueError):
        service.extract("Python document", [])


def test_invalid_field_name(mock_extraction_service):
    service, _ = mock_extraction_service

    with pytest.raises(ValueError):
        service.extract("Python document", ["creator", " "])


def test_invalid_json_response(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = "This is not JSON"

    with pytest.raises(ValueError, match="invalid JSON"):
        service.extract("Python document", ["creator"])


def test_missing_requested_fields(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = '{"creator": "Guido"}'

    with pytest.raises(ValueError, match="Missing requested fields"):
        service.extract(
            "Python document",
            ["creator", "release_year"]
        )


def test_non_object_json_response(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = '["Python", "Java"]'

    with pytest.raises(ValueError, match="JSON object"):
        service.extract("Programming languages", ["creator"])

def test_markdown_wrapped_json(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = (
        '```json\n'
        '{"creator": "Guido van Rossum"}\n'
        '```'
    )

    result = service.extract(
        "Python was created by Guido van Rossum.",
        ["creator"]
    )

    assert result["creator"] == "Guido van Rossum"


def test_json_with_whitespace(mock_extraction_service):
    service, mock_llm = mock_extraction_service

    mock_llm.generate_answer.return_value = (
        '  \n{"creator": "Guido van Rossum"}\n  '
    )

    result = service.extract(
        "Python was created by Guido van Rossum.",
        ["creator"]
    )

    assert result["creator"] == "Guido van Rossum"
