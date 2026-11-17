
import re

from rank_bm25 import BM25Okapi


class KeywordSearchService:
    """
    Perform keyword-based document retrieval using BM25.
    """

    def __init__(self):
        self.documents = []
        self.bm25 = None

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Normalize text into searchable tokens."""

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        return re.findall(r"\b\w+\b", text.lower())

    def index_documents(self, documents: list[dict]) -> int:
        """
        Index document chunks for BM25 search.
        Each document must contain a non-empty text field.
        """

        if not isinstance(documents, list):
            raise TypeError("Documents must be a list.")

        indexed_documents = []
        tokenized_documents = []

        for document in documents:
            if not isinstance(document, dict):
                raise TypeError("Each document must be a dictionary.")

            text = document.get("text")

            if not isinstance(text, str):
                raise ValueError("Every document must contain text.")

            if not text.strip():
                raise ValueError("Document text cannot be empty.")

            tokens = self.tokenize(text)

            if not tokens:
                raise ValueError("Document must contain searchable words.")

            indexed_documents.append(document.copy())
            tokenized_documents.append(tokens)

        self.documents = indexed_documents

        self.bm25 = (
            BM25Okapi(tokenized_documents)
            if tokenized_documents else None
        )

        return len(self.documents)

    def search(
        self,
        query: str,
        limit: int = 5
    ) -> list[dict]:
        """Return the highest-ranked keyword search results."""

        if not isinstance(query, str):
            raise TypeError("Search query must be a string.")

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        query_tokens = self.tokenize(query)

        if not query_tokens or self.bm25 is None:
            return []

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices:
            if scores[index] <= 0:
                continue

            results.append({
                "rank": len(results) + 1,
                "score": float(scores[index]),
                "document": self.documents[index]
            })

            if len(results) >= limit:
                break

        return results
