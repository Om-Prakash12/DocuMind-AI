
from fastapi import FastAPI

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
