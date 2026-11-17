
from backend.app.services.document_processor import process_document
from backend.app.services.embedding_service import EmbeddingService


class DocumentEmbeddingPipeline:
    """
    Process documents and generate embeddings for their chunks.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def process(
        self,
        file_path: str,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ) -> dict:

        # Step 1: Extract, clean and chunk the document
        document = process_document(
            file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunks = document["chunks"]

        if not chunks:
            document["embedding_dimension"] = (
                self.embedding_service.embedding_dimension
            )
            document["embedded_chunks"] = []
            return document

        # Step 2: Collect chunk text
        chunk_texts = [
            chunk["text"] for chunk in chunks
        ]

        # Step 3: Generate embeddings in batches
        embeddings = self.embedding_service.generate_embeddings(
            chunk_texts
        )

        # Step 4: Attach vectors to corresponding chunks
        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append({
                **chunk,
                "embedding": embedding
            })

        # Step 5: Return the completed result
        return {
            **document,
            "embedding_dimension": (
                self.embedding_service.embedding_dimension
            ),
            "embedded_chunks": embedded_chunks
        }
