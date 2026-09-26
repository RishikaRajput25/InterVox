from app.services.embedding.embedder import embedding_service
from app.services.vectorstore.chroma import get_collection


def search_documents(
    query: str,
    top_k: int = 5,
) -> list[dict]:

    if not query.strip():
        return []

    collection = get_collection()

    # Convert user question into embedding
    query_embedding = embedding_service.embed_text(
        query
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    search_results = []

    for index in range(len(documents)):
        search_results.append({
            "chunk_id": ids[index],
            "text": documents[index],
            "metadata": metadatas[index],
            "distance": distances[index],
        })

    return search_results