from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    INDEXED = "indexed"
    FAILED = "failed"


class Document(BaseModel):
    document_id: str
    original_filename: str
    stored_filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: DocumentStatus = DocumentStatus.UPLOADED
    processing_error: str | None = None