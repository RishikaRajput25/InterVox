from pathlib import Path

from app.services.document.extractor import extract_document
from app.services.document.cleaner import clean_text
from app.services.document.chunker import create_chunk_records
from app.services.embedding.embedder import embedding_service


DOCUMENT_PATH = Path(
    "uploads/c0fc6f64-bd70-4eb7-86ff-65425353ecc3.pdf"
)


def main():
    # 1. Extract PDF pages
    pages = extract_document(DOCUMENT_PATH)

    # 2. Clean each page
    cleaned_pages = []

    for page in pages:
        cleaned_pages.append({
            "page_number": page["page_number"],
            "text": clean_text(page["text"]),
        })

    # 3. Create chunks
    chunks = create_chunk_records(
        pages=cleaned_pages,
        document_id="b9356078-d9f5-4e06-ac10-13bc59510cab",
        filename="StyleMirror_Complete_Project_Documentation.pdf",
    )

    print("Total chunks:", len(chunks))

    # 4. Extract chunk text
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 5. Generate embeddings
    embeddings = embedding_service.embed_texts(texts)

    print("Total embeddings:", len(embeddings))

    # 6. Verify dimensions
    if embeddings:
        print(
            "Embedding dimension:",
            len(embeddings[0])
        )

    # 7. Verify every chunk has an embedding
    print(
        "Chunks and embeddings match:",
        len(chunks) == len(embeddings)
    )

    # 8. Show first chunk information
    if chunks:
        print("\nFirst chunk:")
        print(chunks[0]["text"][:300])

        print("\nFirst embedding first 5 values:")
        print(embeddings[0][:5])


if __name__ == "__main__":
    main()