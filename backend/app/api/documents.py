from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.models.document import Document, DocumentStatus
from app.services.document.processor import document_processor
from app.services.document.registry import document_registry

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def process_document_in_background(
    document_id: str,
    file_path: str,
    filename: str,
) -> None:
    document = document_registry.get(document_id)

    if document is None:
        return

    try:
        document_processor.process(
            file_path=file_path,
            document_id=document_id,
            filename=filename,
        )

        document.status = DocumentStatus.INDEXED
        document.processing_error = None

        document_registry.update(document)

        print(
            f"Document {document_id} indexed successfully."
        )

    except Exception as error:
        document.status = DocumentStatus.FAILED
        document.processing_error = str(error)

        document_registry.update(document)

        print(
            f"Document {document_id} processing failed: {error}"
        )


@router.post("/upload", response_model=Document)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are allowed"
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB"
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    document_id = str(uuid4())
    safe_filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / safe_filename
    file_path.write_bytes(file_content)

    document = Document(
        document_id=document_id,
        original_filename=file.filename,
        stored_filename=safe_filename,
        file_type=extension.lstrip("."),
        file_size=len(file_content),
        status=DocumentStatus.PROCESSING,
    )

    document_registry.add(document)

    background_tasks.add_task(
        process_document_in_background,
        document_id,
        str(file_path),
        file.filename,
    )

    return document


@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str):
    document = document_registry.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document