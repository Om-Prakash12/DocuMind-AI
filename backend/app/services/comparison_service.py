
from backend.app.services.llm_service import LLMService


class DocumentComparisonService:
    """
    Compare two documents using a local Ollama LLM.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def compare(
        self,
        document_a: str,
        document_b: str
    ) -> str:

        if not isinstance(document_a, str):
            raise TypeError("Document A must be a string.")

        if not isinstance(document_b, str):
            raise TypeError("Document B must be a string.")

        if not document_a.strip():
            raise ValueError("Document A cannot be empty.")

        if not document_b.strip():
            raise ValueError("Document B cannot be empty.")

        context = f"""
DOCUMENT A:
{document_a}

DOCUMENT B:
{document_b}
"""

        query = """
Compare Document A and Document B.

Organize your response into these sections:

1. Common Information
2. Key Differences
3. Unique Information in Document A
4. Unique Information in Document B
5. Overall Comparison Summary

Rules:
- Use only information from the two documents.
- Do not invent facts.
- Preserve important names, dates and numbers.
- Clearly distinguish information from each document.
- If a comparison cannot be established, say so.
"""

        return self.llm_service.generate_answer(
            query=query,
            context=context
        )
