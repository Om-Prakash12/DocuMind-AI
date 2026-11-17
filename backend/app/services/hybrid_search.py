
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore
from backend.app.services.keyword_search import KeywordSearchService
from backend.app.services.ranking_service import ReciprocalRankFusion


class HybridSearchService:
    """
    Combine semantic search and BM25 keyword search
    using Reciprocal Rank Fusion.
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

        # Retrieve additional candidates before fusion
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

        # 2. Retrieve documents for BM25 indexing
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
            limit=limit
        )

        # 5. Return standardized search results
        return [
            {
                "rank": result["rank"],
                "chunk_id": result["document"].get("chunk_id"),
                "document": result["document"].get("document_filename"),
                "text": result["document"].get("text", ""),
                "score": result["score"],
                "sources": result["document"].get("sources", [])
            }
            for result in fused_results
        ]

    def close(self):
        """Close the Qdrant connection."""
        self.vector_store.close()
