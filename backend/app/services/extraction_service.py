
import json

from backend.app.services.llm_service import LLMService


class InformationExtractionService:
    """
    Extract structured information from documents using Ollama.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def extract(
        self,
        text: str,
        fields: list[str]
    ) -> dict:

        if not isinstance(text, str):
            raise TypeError("Document text must be a string.")

        if not text.strip():
            raise ValueError("Document text cannot be empty.")

        if not isinstance(fields, list):
            raise TypeError("Fields must be a list.")

        if not fields:
            raise ValueError("At least one field is required.")

        if any(
            not isinstance(field, str) or not field.strip()
            for field in fields
        ):
            raise ValueError("Every field must be a non-empty string.")

        query = f"""
Extract the following fields from the document:

{json.dumps(fields)}

Return ONLY a valid JSON object.

Rules:
1. Use only information present in the document.
2. Never invent missing values.
3. Use null when a field is not available.
4. Preserve names, dates and numbers accurately.
5. Do not include Markdown code fences.
"""

        
        response = self.llm_service.generate_answer(
            query=query,
            context=text
        )

        # Remove Markdown code fences if present.
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.split(
                "\n", 1
            )[1]

            if cleaned_response.rstrip().endswith("```"):
                cleaned_response = cleaned_response.rstrip()[:-3]

        cleaned_response = cleaned_response.strip()

        try:
            result = json.loads(cleaned_response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "The LLM returned invalid JSON."
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "The extracted result must be a JSON object."
            )

        missing_fields = set(fields) - set(result.keys())

        if missing_fields:
            raise ValueError(
                f"Missing requested fields: {sorted(missing_fields)}"
            )

        return result
