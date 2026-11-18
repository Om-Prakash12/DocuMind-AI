
from backend.app.services.embedding_pipeline import (
    DocumentEmbeddingPipeline
)
from backend.app.services.vector_store import VectorStore


class DocumentStoragePipeline:
    """
    Process documents, generate embeddings,
    and store them in Qdrant.
    """

    def __init__(
        self,
        storage_path: str = "storage/qdrant"
    ):
        self.embedding_pipeline = DocumentEmbeddingPipeline()

        self.vector_store = VectorStore(
            storage_path=storage_path
        )

    def ingest(
        self,
        file_path: str,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        display_filename: str | None = None
    ) -> dict:

        # Step 1: Process document and generate embeddings
        document = self.embedding_pipeline.process(
            file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        # Step 2: Preserve the original uploaded filename
        if display_filename:
            for chunk in document["embedded_chunks"]:
                chunk["document_filename"] = display_filename

        # Step 3: Store embedded chunks in Qdrant
        stored_count = self.vector_store.add_documents(
            document["embedded_chunks"]
        )

        # Step 4: Return ingestion summary
        return {
            "filename": display_filename or document["filename"],
            "file_type": document["file_type"],
            "total_chunks": document["total_chunks"],
            "stored_vectors": stored_count,
            "embedding_dimension": document["embedding_dimension"],
            "status": "success"
        }

    def close(self):
        """Close the Qdrant connection."""
        self.vector_store.close()
