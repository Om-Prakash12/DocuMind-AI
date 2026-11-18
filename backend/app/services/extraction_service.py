
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
You are an accurate information extraction assistant.

Extract the requested fields from the provided document.

Requested fields:
{json.dumps(fields)}

Instructions:
1. Read the entire document carefully before extracting information.
2. Interpret field names by their meaning, not only by exact word matches.
3. Identify information expressed using equivalent words or phrases.
4. Extract all relevant information when multiple values are available.
5. Use only evidence explicitly supported by the document.
6. Never invent, assume, or guess information.
7. Return null only when the document genuinely does not contain the requested information.
8. Preserve names, dates, numbers, and technical terms accurately.
9. Return values as concise strings unless a list is more appropriate.
10. Return ONLY a valid JSON object containing every requested field.
11. Do not include Markdown code fences or explanations.

Example:
If the document says:
"Python is widely used in artificial intelligence and machine learning."

And the requested field is:
"main_applications"

Extract:
"main_applications": "Artificial Intelligence and Machine Learning"
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
