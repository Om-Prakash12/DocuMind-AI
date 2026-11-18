from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.comparison_service import (
    DocumentComparisonService
)

router = APIRouter(
    prefix="/compare",
    tags=["Document Comparison"]
)


class ComparisonRequest(BaseModel):
    document_a: str = Field(
        min_length=1,
        description="Content of the first document"
    )
    document_b: str = Field(
        min_length=1,
        description="Content of the second document"
    )


@router.post("/")
def compare_documents(request: ComparisonRequest):
    try:
        service = DocumentComparisonService()

        result = service.compare(
            document_a=request.document_a,
            document_b=request.document_b
        )

        return {
            "status": "success",
            "comparison": result
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document comparison failed."
        ) from exc