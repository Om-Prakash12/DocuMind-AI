
import numpy as np
import pytest

from backend.app.services.embedding_service import EmbeddingService


@pytest.fixture(scope="module")
def embedding_service():
    return EmbeddingService()


def test_embedding_dimension(embedding_service):
    vector = embedding_service.generate_embedding(
        "DocuMind is an AI document platform."
    )

    assert len(vector) == 384


def test_single_embedding_is_normalized(embedding_service):
    vector = embedding_service.generate_embedding(
        "Artificial intelligence and machine learning."
    )

    assert np.isclose(np.linalg.norm(vector), 1.0, atol=1e-5)


def test_batch_embedding_generation(embedding_service):
    texts = [
        "Python is a programming language.",
        "FastAPI is a Python web framework.",
        "Machine learning uses data."
    ]

    vectors = embedding_service.generate_embeddings(texts)

    assert len(vectors) == 3
    assert all(len(vector) == 384 for vector in vectors)


def test_semantic_similarity(embedding_service):
    texts = [
        "A dog is playing in the garden.",
        "A puppy is running outside.",
        "The stock market closed higher today."
    ]

    vectors = embedding_service.generate_embeddings(texts)

    similar_score = np.dot(vectors[0], vectors[1])
    unrelated_score = np.dot(vectors[0], vectors[2])

    assert similar_score > unrelated_score


def test_empty_single_text(embedding_service):
    with pytest.raises(ValueError):
        embedding_service.generate_embedding("")


def test_invalid_single_text(embedding_service):
    with pytest.raises(TypeError):
        embedding_service.generate_embedding(123)


def test_empty_batch(embedding_service):
    assert embedding_service.generate_embeddings([]) == []


def test_invalid_batch(embedding_service):
    with pytest.raises(TypeError):
        embedding_service.generate_embeddings("not a list")


def test_batch_with_empty_text(embedding_service):
    with pytest.raises(ValueError):
        embedding_service.generate_embeddings(["Hello", ""])
