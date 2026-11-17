
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore


class SemanticSearchService:
    """
    Search stored document chunks using semantic similarity.
    """

    def __init__(
        self,
        storage_path: str = "storage/qdrant"
    ):
        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore(
            storage_path=storage_path
        )

    
    def search(
        self,
        query: str,
        limit: int = 5,
        document_filename: str | None = None
    ) -> list[dict]:
        """Search documents semantically with optional file filtering."""

        if not isinstance(query, str):
            raise TypeError("Search query must be a string.")

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit <= 0:
            raise ValueError("Search limit must be greater than zero.")

        if document_filename is not None:
            if not isinstance(document_filename, str):
                raise TypeError("Document filename must be a string.")

            if not document_filename.strip():
                raise ValueError("Document filename cannot be empty.")

        query_vector = self.embedding_service.generate_embedding(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=limit,
            document_filename=document_filename
        )

        return [
            {
                "document": result["payload"].get("document_filename"),
                "text": result["payload"].get("text", ""),
                "score": result["score"],
                "sources": result["payload"].get("sources", []),
                "chunk_id": result["payload"].get("chunk_id")
            }
            for result in results
        ]


    def close(self):
        """Close the Qdrant connection."""
        self.vector_store.close()
