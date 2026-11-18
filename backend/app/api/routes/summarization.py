
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.summarization_service import (
    SummarizationService
)

router = APIRouter(
    prefix="/summarize",
    tags=["Summarization"]
)


class SummarizationRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="Document text to summarize"
    )

    summary_type: str = Field(
        default="short",
        description="Summary type: short or detailed"
    )


@router.post("/")
def summarize_document(request: SummarizationRequest):

    try:
        service = SummarizationService()

        summary = service.summarize(
            text=request.text,
            summary_type=request.summary_type
        )

        return {
            "status": "success",
            "summary_type": request.summary_type,
            "summary": summary
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document summarization failed."
        ) from exc
