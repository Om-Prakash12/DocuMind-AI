
from fastapi import FastAPI

from backend.app.api.routes.documents import router as documents_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.summarization import router as summarization_router
from backend.app.api.routes.comparison import router as comparison_router
from backend.app.api.routes.extraction import router as extraction_router
app = FastAPI(
    title="DocuMind API",
    description="AI-powered Document Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind AI",
        "status": "running"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "DocuMind AI",
        "version": "1.0.0"
    }


app.include_router(
    documents_router,
    prefix="/api/v1"
)

app.include_router(
    chat_router,
    prefix="/api/v1"
)

app.include_router(
    summarization_router, 
    prefix="/api/v1"
    )
app.include_router(comparison_router, 
                   prefix="/api/v1"
                   )
app.include_router(extraction_router, prefix="/api/v1")