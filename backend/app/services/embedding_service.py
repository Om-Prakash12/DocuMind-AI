
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generate semantic embeddings using Sentence Transformers.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        if not isinstance(texts, list):
            raise TypeError("Input must be a list of strings.")

        if not texts:
            return []

        if any(not isinstance(text, str) for text in texts):
            raise TypeError("Every item must be a string.")

        if any(not text.strip() for text in texts):
            raise ValueError("Texts cannot contain empty strings.")

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False
        )

        return embeddings.tolist()

    @property
    def embedding_dimension(self) -> int:
        """Return the vector dimension of the model."""

        return self.model.get_sentence_embedding_dimension()
