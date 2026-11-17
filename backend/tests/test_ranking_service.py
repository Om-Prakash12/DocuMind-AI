
import pytest

from backend.app.services.ranking_service import ReciprocalRankFusion


@pytest.fixture
def rrf():
    return ReciprocalRankFusion(k=60)


def make_result(chunk_id, text):
    return {
        "document": {
            "chunk_id": chunk_id,
            "text": text
        }
    }


def test_fuse_two_result_lists(rrf):
    semantic_results = [
        make_result("A", "Python AI"),
        make_result("B", "FastAPI backend")
    ]

    keyword_results = [
        make_result("B", "FastAPI backend"),
        make_result("C", "Machine learning")
    ]

    results = rrf.fuse(
        semantic_results,
        keyword_results
    )

    assert len(results) == 3
    assert results[0]["document"]["chunk_id"] == "B"


def test_shared_document_gets_higher_score(rrf):
    semantic_results = [
        make_result("A", "Python AI"),
        make_result("B", "FastAPI")
    ]

    keyword_results = [
        make_result("B", "FastAPI"),
        make_result("C", "Machine learning")
    ]

    results = rrf.fuse(
        semantic_results,
        keyword_results
    )

    scores = {
        item["document"]["chunk_id"]: item["score"]
        for item in results
    }

    assert scores["B"] > scores["A"]
    assert scores["B"] > scores["C"]


def test_single_result_list(rrf):
    results = rrf.fuse([
        make_result("A", "Python programming")
    ])

    assert len(results) == 1
    assert results[0]["document"]["chunk_id"] == "A"


def test_empty_result_lists(rrf):
    assert rrf.fuse([], []) == []


def test_result_limit(rrf):
    results = rrf.fuse(
        [
            make_result("A", "One"),
            make_result("B", "Two"),
            make_result("C", "Three")
        ],
        limit=2
    )

    assert len(results) == 2


def test_invalid_limit(rrf):
    with pytest.raises(ValueError):
        rrf.fuse([], limit=0)


def test_invalid_rrf_constant():
    with pytest.raises(ValueError):
        ReciprocalRankFusion(k=0)


def test_missing_chunk_id(rrf):
    with pytest.raises(ValueError):
        rrf.fuse([
            {"document": {"text": "Missing ID"}}
        ])


def test_duplicate_document_in_same_list(rrf):
    results = rrf.fuse([
        make_result("A", "Python"),
        make_result("A", "Python")
    ])

    assert len(results) == 1
    assert results[0]["score"] == pytest.approx(1 / 61)
