
from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient, models


class VectorStore:
    """
    Manage document vectors using local Qdrant storage.
    """

    def __init__(
        self,
        storage_path: str = "storage/qdrant",
        collection_name: str = "documind_documents",
        vector_size: int = 384
    ):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.collection_name = collection_name
        self.vector_size = vector_size

        self.client = QdrantClient(
            path=str(self.storage_path)
        )

        self.create_collection()

    def create_collection(self):
        """Create the collection if it doesn't already exist."""

        if not self.client.collection_exists(
            self.collection_name
        ):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )

    def add_documents(
        self,
        embedded_chunks: list[dict]
    ) -> int:
        """Store document chunks and their embeddings."""

        if not embedded_chunks:
            return 0

        points = []

        for chunk in embedded_chunks:
            embedding = chunk.get("embedding")

            if not isinstance(embedding, list):
                raise ValueError("Each chunk must have an embedding list.")

            if len(embedding) != self.vector_size:
                raise ValueError(
                    f"Expected {self.vector_size} vector values, "
                    f"received {len(embedding)}."
                )

            payload = {
                key: value
                for key, value in chunk.items()
                if key != "embedding"
            }

            points.append(
                models.PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

        return len(points)

    
    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        document_filename: str | None = None
    ) -> list[dict]:
        """Search vectors, optionally filtering by document filename."""

        if len(query_vector) != self.vector_size:
            raise ValueError(
                f"Expected query vector size {self.vector_size}."
            )

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        query_filter = None

        if document_filename is not None:
            if not document_filename.strip():
                raise ValueError("Document filename cannot be empty.")

            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_filename",
                        match=models.MatchValue(
                            value=document_filename
                        )
                    )
                ]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True
        ).points

        return [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload
            }
            for point in results
        ]


    def count_documents(self) -> int:
        """Return the number of stored vector points."""

        result = self.client.count(
            collection_name=self.collection_name,
            exact=True
        )

        return result.count
    
    def get_all_documents(self, page_size: int = 100) -> list[dict]:
        """
        Retrieve all stored document payloads from Qdrant.
        Uses pagination to handle larger collections.
        """

        if page_size <= 0:
            raise ValueError("Page size must be greater than zero.")

        documents = []
        offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=page_size,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )

            for point in points:
                documents.append({
                    "qdrant_id": str(point.id),
                    **(point.payload or {})
                })

            if next_offset is None:
                break

            offset = next_offset

        return documents

    def close(self):
        """Close the local Qdrant client."""

        self.client.close()
