# from pathlib import Path

# from app.services.document.extractor import extract_document
# from app.services.document.cleaner import clean_text
# from app.services.document.chunker import create_chunk_records
# from app.services.embedding.embedder import embedding_service
# from app.services.vectorstore.chroma import get_collection


# DOCUMENT_PATH = Path(
#     "uploads/c0fc6f64-bd70-4eb7-86ff-65425353ecc3.pdf"
# )

# DOCUMENT_ID = "b9356078-d9f5-4e06-ac10-13bc59510cab"

# FILENAME = "StyleMirror_Complete_Project_Documentation.pdf"


# def main():
#     print("Starting document indexing...\n")

#     # 1. Extract
#     print("1. Extracting document...")

#     pages = extract_document(DOCUMENT_PATH)

#     print("Pages:", len(pages))

#     # 2. Clean
#     print("\n2. Cleaning text...")

#     cleaned_pages = []

#     for page in pages:
#         cleaned_pages.append({
#             "page_number": page["page_number"],
#             "text": clean_text(page["text"]),
#         })

#     # 3. Chunk
#     print("\n3. Creating chunks...")

#     chunks = create_chunk_records(
#         pages=cleaned_pages,
#         document_id=DOCUMENT_ID,
#         filename=FILENAME,
#     )

#     print("Chunks:", len(chunks))

#     # 4. Generate embeddings
#     print("\n4. Generating embeddings...")

#     texts = [
#         chunk["text"]
#         for chunk in chunks
#     ]

#     embeddings = embedding_service.embed_texts(texts)

#     print("Embeddings:", len(embeddings))

#     # 5. Get Chroma collection
#     print("\n5. Connecting to ChromaDB...")

#     collection = get_collection()

#     # 6. Prepare data
#     ids = [
#         chunk["chunk_id"]
#         for chunk in chunks
#     ]

#     metadatas = [
#         {
#             "document_id": chunk["document_id"],
#             "filename": chunk["filename"],
#             "page_number": chunk["page_number"],
#         }
#         for chunk in chunks
#     ]

#     # 7. Store chunks + embeddings + metadata
#     print("\n6. Storing chunks in ChromaDB...")

#     collection.upsert(
#         ids=ids,
#         documents=texts,
#         embeddings=embeddings,
#         metadatas=metadatas,
#     )

#     print("Indexing completed.")

#     # 8. Verify
#     print("\n7. Verification")

#     print(
#         "Total documents in collection:",
#         collection.count()
#     )

#     result = collection.get(
#         ids=[ids[0]]
#     )

#     print("\nFirst stored chunk:")
#     print(result["documents"][0][:300])

#     print("\nFirst stored metadata:")
#     print(result["metadatas"][0])


# if __name__ == "__main__":
#     main()



from pathlib import Path

from app.services.document.extractor import extract_document
from app.services.document.cleaner import clean_text
from app.services.document.chunker import create_chunk_records
from app.services.embedding.embedder import embedding_service
from app.services.vectorstore.chroma import get_collection


DOCUMENT_PATH = Path(
    "uploads/9b72579b-160a-44de-9927-10b4096d3d88.pdf"
)

DOCUMENT_ID = "resume-rishika-001"

FILENAME = "ResumeML.pdf"


def main():

    print("Starting document indexing...\n")

    # ---------------------------------------------
    # 1. Extract document
    # ---------------------------------------------

    print("1. Extracting document...")

    pages = extract_document(
        DOCUMENT_PATH
    )

    print(
        "Pages:",
        len(pages)
    )

    # ---------------------------------------------
    # 2. Clean text
    # ---------------------------------------------

    print("\n2. Cleaning text...")

    cleaned_pages = []

    for page in pages:

        cleaned_pages.append({
            "page_number": page["page_number"],
            "text": clean_text(
                page["text"]
            ),
        })

    # ---------------------------------------------
    # 3. Create chunks
    # ---------------------------------------------

    print("\n3. Creating chunks...")

    chunks = create_chunk_records(
        pages=cleaned_pages,
        document_id=DOCUMENT_ID,
        filename=FILENAME,
    )

    print(
        "Chunks:",
        len(chunks)
    )

    # ---------------------------------------------
    # 4. Generate embeddings
    # ---------------------------------------------

    print("\n4. Generating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_texts(
        texts
    )

    print(
        "Embeddings:",
        len(embeddings)
    )

    # ---------------------------------------------
    # 5. Connect to ChromaDB
    # ---------------------------------------------

    print("\n5. Connecting to ChromaDB...")

    collection = get_collection()

    # ---------------------------------------------
    # 6. Prepare metadata
    # ---------------------------------------------

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
        }
        for chunk in chunks
    ]

    # ---------------------------------------------
    # 7. Store in ChromaDB
    # ---------------------------------------------

    print(
        "\n6. Storing chunks in ChromaDB..."
    )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        "Indexing completed."
    )

    # ---------------------------------------------
    # 8. Verification
    # ---------------------------------------------

    print("\n7. Verification")

    print(
        "Total chunks in collection:",
        collection.count()
    )

    result = collection.get(
        ids=[ids[0]]
    )

    print(
        "\nFirst stored chunk:"
    )

    print(
        result["documents"][0][:300]
    )

    print(
        "\nFirst stored metadata:"
    )

    print(
        result["metadatas"][0]
    )


if __name__ == "__main__":
    main()