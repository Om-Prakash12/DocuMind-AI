from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.extraction_service import (
    InformationExtractionService
)

router = APIRouter(
    prefix="/extract",
    tags=["Information Extraction"]
)


class ExtractionRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="Document text for information extraction"
    )
    fields: list[str] = Field(
        min_length=1,
        description="Information fields to extract"
    )


@router.post("/")
def extract_information(request: ExtractionRequest):
    try:
        service = InformationExtractionService()

        result = service.extract(
            text=request.text,
            fields=request.fields
        )

        return {
            "status": "success",
            "extracted_information": result
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Information extraction failed."
        ) from exc