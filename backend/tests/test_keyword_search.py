
import pytest

from backend.app.services.keyword_search import KeywordSearchService


@pytest.fixture
def keyword_service():
    service = KeywordSearchService()

    documents = [
        {
            "chunk_id": "chunk-1",
            "text": "Python is widely used for artificial intelligence and machine learning.",
            "document_filename": "ai_guide.txt"
        },
        {
            "chunk_id": "chunk-2",
            "text": "FastAPI is a modern Python framework for building web APIs.",
            "document_filename": "backend_guide.txt"
        },
        {
            "chunk_id": "chunk-3",
            "text": "Cricket is a popular sport played between two teams.",
            "document_filename": "sports_guide.txt"
        }
    ]

    service.index_documents(documents)

    return service


def test_index_documents(keyword_service):
    assert len(keyword_service.documents) == 3


def test_exact_keyword_search(keyword_service):
    results = keyword_service.search("FastAPI")

    assert len(results) > 0
    assert results[0]["document"]["document_filename"] == "backend_guide.txt"


def test_keyword_ranking(keyword_service):
    results = keyword_service.search("Python")

    assert results[0]["document"]["document_filename"] == "ai_guide.txt"


def test_search_limit(keyword_service):
    results = keyword_service.search("Python", limit=1)

    assert len(results) == 1


def test_no_matching_keyword(keyword_service):
    results = keyword_service.search("blockchain")

    assert results == []


def test_empty_query(keyword_service):
    with pytest.raises(ValueError):
        keyword_service.search("")


def test_invalid_query(keyword_service):
    with pytest.raises(TypeError):
        keyword_service.search(123)


def test_invalid_limit(keyword_service):
    with pytest.raises(ValueError):
        keyword_service.search("Python", limit=0)


def test_empty_document_list():
    service = KeywordSearchService()

    assert service.index_documents([]) == 0
    assert service.search("Python") == []


def test_invalid_document():
    service = KeywordSearchService()

    with pytest.raises(ValueError):
        service.index_documents([{"text": ""}])


def test_tokenization():
    service = KeywordSearchService()

    result = service.tokenize("Python, FASTAPI and AI!")

    assert result == ["python", "fastapi", "and", "ai"]
