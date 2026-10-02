from pathlib import Path

from app.services.document.cleaner import clean_text
from app.services.document.chunker import create_chunk_records
from app.services.document.extractor import extract_document
from app.services.embedding.embedder import embedding_service
from app.services.vectorstore.chroma import add_document_chunks


class DocumentProcessor:
    def process(
        self,
        file_path: str,
        document_id: str,
        filename: str,
    ) -> int:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document file not found: {file_path}"
            )

        # 1. Extract text
        pages = extract_document(path)

        if not pages:
            raise ValueError(
                "No text could be extracted from the document"
            )

        # 2. Clean extracted text
        cleaned_pages = []

        for page in pages:
            cleaned_text = clean_text(page["text"])

            if cleaned_text:
                cleaned_pages.append({
                    "page_number": page["page_number"],
                    "text": cleaned_text,
                })

        if not cleaned_pages:
            raise ValueError(
                "Document contains no usable text"
            )

        # 3. Create chunks with citation metadata
        chunk_records = create_chunk_records(
            pages=cleaned_pages,
            document_id=document_id,
            filename=filename,
        )

        if not chunk_records:
            raise ValueError(
                "No chunks could be created from the document"
            )

        # 4. Generate embeddings in batch
        texts = [
            chunk["text"]
            for chunk in chunk_records
        ]

        embeddings = embedding_service.embed_texts(texts)

        # 5. Store chunks + embeddings + metadata in ChromaDB
        add_document_chunks(
            chunk_records=chunk_records,
            embeddings=embeddings,
        )

        return len(chunk_records)


document_processor = DocumentProcessor()