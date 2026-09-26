# from pathlib import Path
# from uuid import uuid4

# from fastapi import APIRouter, File, HTTPException, UploadFile


# router = APIRouter(
#     prefix="/documents",
#     tags=["Documents"]
# )


# UPLOAD_DIR = Path("uploads")

# ALLOWED_EXTENSIONS = {
#     ".pdf",
#     ".docx",
#     ".txt",
# }

# MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     if not file.filename:
#         raise HTTPException(
#             status_code=400,
#             detail="No file selected"
#         )

#     extension = Path(file.filename).suffix.lower()

#     if extension not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF, DOCX and TXT files are allowed"
#         )

#     file_content = await file.read()

#     if len(file_content) > MAX_FILE_SIZE:
#         raise HTTPException(
#             status_code=400,
#             detail="File size must be less than 10 MB"
#         )

#     safe_filename = f"{uuid4()}{extension}"

#     file_path = UPLOAD_DIR / safe_filename

#     file_path.write_bytes(file_content)

#     return {
#         "message": "Document uploaded successfully",
#         "filename": file.filename,
#         "stored_filename": safe_filename,
#         "size": len(file_content),
#     }



from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.document import Document


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


@router.post("/upload", response_model=Document)
async def upload_document(file: UploadFile = File(...)):
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
    )

    return document