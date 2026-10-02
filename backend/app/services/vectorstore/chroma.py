import chromadb


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "intervox_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "InterVox document chunks and embeddings"
        },
    )


def add_document_chunks(
    chunk_records: list[dict],
    embeddings: list[list[float]],
) -> None:
    if not chunk_records:
        return

    if len(chunk_records) != len(embeddings):
        raise ValueError(
            "Number of chunk records and embeddings must match"
        )

    collection = get_collection()

    ids = [
        chunk["chunk_id"]
        for chunk in chunk_records
    ]

    documents = [
        chunk["text"]
        for chunk in chunk_records
    ]

    metadatas = [
        {
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
        }
        for chunk in chunk_records
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )