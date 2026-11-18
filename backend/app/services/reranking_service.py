
from sentence_transformers import CrossEncoder


class RerankingService:
    """
    Rerank retrieved document chunks using a Cross-Encoder.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model_name = model_name

        self.model = CrossEncoder(
            model_name,
            max_length=512
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5
    ) -> list[dict]:
        """
        Score query-document pairs and return the most
        relevant documents in descending score order.
        """

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if not isinstance(documents, list):
            raise TypeError("Documents must be a list.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not documents:
            return []

        for document in documents:
            if not isinstance(document, dict):
                raise TypeError("Each document must be a dictionary.")

            if not isinstance(document.get("text"), str):
                raise ValueError("Every document must contain text.")

            if not document["text"].strip():
                raise ValueError("Document text cannot be empty.")

        # Create query-document pairs
        pairs = [
            [query, document["text"]]
            for document in documents
        ]

        # Generate relevance scores
        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False
        )

        # Attach scores without modifying original documents
        ranked_documents = []

        for document, score in zip(documents, scores):
            ranked_documents.append({
                **document,
                "rerank_score": float(score)
            })

        # Sort by relevance
        ranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return ranked_documents[:top_k]
