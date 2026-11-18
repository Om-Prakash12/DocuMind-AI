
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["Chat"])

# Reuse the RAG service instead of reloading AI models
# for every incoming request.
_rag_service = None


def get_rag_service():
    global _rag_service

    if _rag_service is None:
        _rag_service = RAGService()

    return _rag_service


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Question about uploaded documents"
    )
    limit: int = Field(default=5, ge=1, le=20)
    document_filename: str | None = None


@router.post("/")
def chat(request: ChatRequest):

    try:
        service = get_rag_service()

        result = service.answer_question(
            query=request.query,
            limit=request.limit,
            document_filename=request.document_filename
        )

        return {
            "status": "success",
            "data": result
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to process your question."
        ) from exc
