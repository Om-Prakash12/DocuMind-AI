
from backend.app.services.hybrid_search import HybridSearchService
from backend.app.services.llm_service import LLMService


class RAGService:
    """
    Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        storage_path: str = "storage/qdrant",
        relevance_threshold: float = 0.0
    ):
        self.search_service = HybridSearchService(
            storage_path=storage_path
        )
        self.llm_service = LLMService()
        self.relevance_threshold = relevance_threshold

    def answer_question(
        self,
        query: str,
        limit: int = 5,
        document_filename: str | None = None
    ) -> dict:

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        results = self.search_service.search(
            query=query,
            limit=limit,
            document_filename=document_filename
        )

        # Keep only sufficiently relevant results.
        relevant_results = [
            result for result in results
            if result.get("score") is not None
            and result["score"] > self.relevance_threshold
        ]

        if not relevant_results:
            return {
                "question": query,
                "answer": (
                    "The provided documents do not contain "
                    "enough information to answer this question."
                ),
                "sources": []
            }

        context_parts = []
        sources = []

        for index, result in enumerate(
            relevant_results, start=1
        ):
            context_parts.append(
                f"[Source {index}]\n{result['text']}"
            )

            sources.append({
                "document": result.get("document"),
                "chunk_id": result.get("chunk_id"),
                "score": result.get("score"),
                "references": result.get("sources", [])
            })

        context = "\n\n".join(context_parts)

        answer = self.llm_service.generate_answer(
            query=query,
            context=context
        )

        return {
            "question": query,
            "answer": answer,
            "sources": sources
        }

    def close(self):
        self.search_service.close()
