
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.services.storage_pipeline import (
    DocumentStoragePipeline
)

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("storage/uploads")
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if not filename or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / safe_filename

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        file_path.write_bytes(content)

        pipeline = DocumentStoragePipeline()

        try:
            result = pipeline.ingest(
               str(file_path),
               display_filename=filename
            )
        finally:
            pipeline.close()

        return {
            "message": "Document uploaded and indexed successfully.",
            "original_filename": filename,
            "stored_filename": safe_filename,
            "result": result
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(exc)}"
        ) from exc

    finally:
        await file.close()

@router.get("/")
def list_documents():
    from backend.app.services.vector_store import VectorStore

    store = VectorStore()

    try:
        documents = store.get_all_documents()

        # Group chunks by original filename.
        grouped = {}

        for document in documents:
            filename = document.get("document_filename", "unknown")

            if filename not in grouped:
                grouped[filename] = {
                    "filename": filename,
                    "total_chunks": 0,
                    "chunks": []
                }

            grouped[filename]["total_chunks"] += 1
            grouped[filename]["chunks"].append(
                document.get("chunk_id")
            )

        return {
            "total_documents": len(grouped),
            "documents": list(grouped.values())
        }

    finally:
        store.close()
