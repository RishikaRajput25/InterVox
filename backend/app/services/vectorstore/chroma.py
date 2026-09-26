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