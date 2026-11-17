
import pytest

from backend.app.services.vector_store import VectorStore


@pytest.fixture
def vector_store(tmp_path):
    store = VectorStore(
        storage_path=str(tmp_path / "qdrant_test"),
        collection_name="test_documents",
        vector_size=384
    )

    yield store
    store.close()


def create_test_chunk(text, vector):
    return {
        "chunk_id": "chunk-001",
        "chunk_index": 1,
        "text": text,
        "word_count": len(text.split()),
        "document_filename": "sample.txt",
        "document_type": "txt",
        "sources": [
            {
                "block_type": "line",
                "line_number": 1
            }
        ],
        "embedding": vector
    }


def test_collection_creation(vector_store):
    assert vector_store.client.collection_exists(
        "test_documents"
    )


def test_add_document(vector_store):
    vector = [1.0] + [0.0] * 383

    chunk = create_test_chunk(
        "DocuMind AI document intelligence",
        vector
    )

    result = vector_store.add_documents([chunk])

    assert result == 1
    assert vector_store.count_documents() == 1


def test_search_document(vector_store):
    vector = [1.0] + [0.0] * 383

    chunk = create_test_chunk(
        "DocuMind AI document intelligence",
        vector
    )

    vector_store.add_documents([chunk])

    results = vector_store.search(
        query_vector=vector,
        limit=5
    )

    assert len(results) == 1
    assert results[0]["payload"]["document_filename"] == "sample.txt"
    assert results[0]["payload"]["text"] == (
        "DocuMind AI document intelligence"
    )


def test_empty_document_insertion(vector_store):
    result = vector_store.add_documents([])

    assert result == 0
    assert vector_store.count_documents() == 0


def test_invalid_vector_dimension(vector_store):
    chunk = create_test_chunk(
        "Invalid vector",
        [1.0, 0.5]
    )

    with pytest.raises(ValueError):
        vector_store.add_documents([chunk])


def test_invalid_search_dimension(vector_store):
    with pytest.raises(ValueError):
        vector_store.search([1.0, 0.5])


def test_invalid_search_limit(vector_store):
    with pytest.raises(ValueError):
        vector_store.search(
            query_vector=[1.0] + [0.0] * 383,
            limit=0
        )

def test_get_all_documents(vector_store):
    chunks = [
        {
            "chunk_id": "chunk-1",
            "text": "Python programming",
            "embedding": [1.0] + [0.0] * 383
        },
        {
            "chunk_id": "chunk-2",
            "text": "Artificial intelligence",
            "embedding": [0.0, 1.0] + [0.0] * 382
        }
    ]

    vector_store.add_documents(chunks)

    documents = vector_store.get_all_documents()

    assert len(documents) == 2
    assert {doc["chunk_id"] for doc in documents} == {
        "chunk-1", "chunk-2"
    }


def test_get_all_documents_empty(vector_store):
    assert vector_store.get_all_documents() == []


def test_invalid_page_size(vector_store):
    with pytest.raises(ValueError):
        vector_store.get_all_documents(page_size=0)
