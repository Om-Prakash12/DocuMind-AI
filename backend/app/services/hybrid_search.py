
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.services.keyword_search import KeywordSearchService
from backend.app.services.ranking_service import ReciprocalRankFusion
from backend.app.services.reranking_service import RerankingService


class HybridSearchService:
    """
    Combine semantic search, BM25, RRF and Cross-Encoder reranking.
    """

    def __init__(
        self,
        storage_path: str = "storage/qdrant"
    ):
        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore(
            storage_path=storage_path
        )

        self.keyword_service = KeywordSearchService()
        self.ranking_service = ReciprocalRankFusion(k=60)
        self.reranking_service = RerankingService()

    def search(
        self,
        query: str,
        limit: int = 5,
        document_filename: str | None = None
    ) -> list[dict]:

        if not isinstance(query, str):
            raise TypeError("Search query must be a string.")

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        if document_filename is not None:
            if not isinstance(document_filename, str):
                raise TypeError("Document filename must be a string.")

            if not document_filename.strip():
                raise ValueError("Document filename cannot be empty.")

        candidate_limit = max(limit * 3, 10)

        # 1. Semantic search
        query_vector = self.embedding_service.generate_embedding(query)

        semantic_results = self.vector_store.search(
            query_vector=query_vector,
            limit=candidate_limit,
            document_filename=document_filename
        )

        semantic_ranked = [
            {"document": result["payload"]}
            for result in semantic_results
        ]

        # 2. Retrieve documents for BM25
        documents = self.vector_store.get_all_documents()

        if document_filename is not None:
            documents = [
                document for document in documents
                if document.get("document_filename") == document_filename
            ]

        # 3. Keyword search
        self.keyword_service.index_documents(documents)

        keyword_results = self.keyword_service.search(
            query=query,
            limit=candidate_limit
        )

        # 4. Combine rankings using RRF
        fused_results = self.ranking_service.fuse(
            semantic_ranked,
            keyword_results,
            limit=candidate_limit
        )

        # 5. Prepare candidates for Cross-Encoder
        candidates = []

        for result in fused_results:
            document = result["document"]

            candidates.append({
                "rank": result["rank"],
                "chunk_id": document.get("chunk_id"),
                "document": document.get("document_filename"),
                "text": document.get("text", ""),
                "rrf_score": result["score"],
                "sources": document.get("sources", [])
            })

        # 6. Rerank candidates using Cross-Encoder
        reranked_results = self.reranking_service.rerank(
            query=query,
            documents=candidates,
            top_k=limit
        )

        # 7. Return final ranked results
        return [
            {
                **{
                    key: value
                    for key, value in result.items()
                    if key != "rerank_score"
                },
                "rank": index,
                "score": result["rerank_score"]
            }
            for index, result in enumerate(
                reranked_results,
                start=1
            )
        ]

    def close(self):
        """Close the Qdrant connection."""
        self.vector_store.close()
