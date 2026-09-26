from app.services.retrieval.semantic_search import search_documents
from app.services.retrieval.keyword_search import search_by_keyword


SEMANTIC_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3


def normalize_semantic_score(distance: float) -> float:
    """
    Convert Chroma distance into a relevance score.

    Lower distance means better semantic similarity.
    We convert it so that higher score means better result.
    """

    return 1 / (1 + distance)


def search_hybrid(
    query: str,
    top_k: int = 5,
) -> list[dict]:

    if not query.strip():
        return []

    # --------------------------------------------------
    # 1. Semantic Search
    # --------------------------------------------------

    semantic_results = search_documents(
        query=query,
        top_k=top_k,
    )

    # --------------------------------------------------
    # 2. Keyword Search
    # --------------------------------------------------

    keyword_results = search_by_keyword(
        query=query,
        top_k=top_k,
    )

    # --------------------------------------------------
    # 3. Combine results
    # --------------------------------------------------

    combined_results = {}

    for result in semantic_results:

        chunk_id = result["chunk_id"]

        semantic_score = normalize_semantic_score(
            result["distance"]
        )

        combined_results[chunk_id] = {
            "chunk_id": chunk_id,
            "text": result["text"],
            "metadata": result["metadata"],
            "semantic_score": semantic_score,
            "keyword_score": 0.0,
        }

    for result in keyword_results:

        chunk_id = result["chunk_id"]

        if chunk_id not in combined_results:

            combined_results[chunk_id] = {
                "chunk_id": chunk_id,
                "text": result["text"],
                "metadata": result["metadata"],
                "semantic_score": 0.0,
                "keyword_score": 0.0,
            }

        combined_results[chunk_id]["keyword_score"] = (
            result["keyword_score"]
        )

    # --------------------------------------------------
    # 4. Calculate Hybrid Score
    # --------------------------------------------------

    for result in combined_results.values():

        result["hybrid_score"] = (
            SEMANTIC_WEIGHT
            * result["semantic_score"]
            +
            KEYWORD_WEIGHT
            * result["keyword_score"]
        )

    # --------------------------------------------------
    # 5. Sort by Hybrid Score
    # --------------------------------------------------

    ranked_results = sorted(
        combined_results.values(),
        key=lambda result: result["hybrid_score"],
        reverse=True,
    )

    return ranked_results[:top_k]