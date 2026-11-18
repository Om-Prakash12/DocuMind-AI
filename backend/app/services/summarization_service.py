
from backend.app.services.llm_service import LLMService


class SummarizationService:
    """
    Summarize documents using a local Ollama LLM.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def summarize(
        self,
        text: str,
        summary_type: str = "short"
    ) -> str:

        if not isinstance(text, str):
            raise TypeError("Document text must be a string.")

        if not text.strip():
            raise ValueError("Document text cannot be empty.")

        if summary_type not in ("short", "detailed"):
            raise ValueError(
                "Summary type must be 'short' or 'detailed'."
            )

        if summary_type == "short":
            instruction = (
                "Create a concise summary in approximately "
                "100 words. Include only the most important ideas."
            )
        else:
            instruction = (
                "Create a detailed summary with clear headings. "
                "Include the main topics, important facts, "
                "key findings and conclusions."
            )

        prompt = f"""
Summarize the following document.

Instructions:
{instruction}

Important rules:
1. Use only information from the document.
2. Do not invent facts.
3. Preserve important names, dates and numbers.
4. If information is unclear, do not guess.

DOCUMENT:
{text}
"""

        return self.llm_service.generate_answer(
            query="Summarize the provided document.",
            context=prompt
        )
