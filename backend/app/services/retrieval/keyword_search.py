import re

from app.services.vectorstore.chroma import get_collection


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase words/tokens.
    """

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


def calculate_keyword_score(
    query_tokens: list[str],
    document_text: str,
) -> float:
    """
    Calculate a simple keyword-overlap score.

    Score = number of unique query words
            found in the document.
    """

    if not query_tokens:
        return 0.0

    document_tokens = set(
        tokenize(document_text)
    )

    matched_tokens = 0

    for token in set(query_tokens):
        if token in document_tokens:
            matched_tokens += 1

    return matched_tokens / len(set(query_tokens))


def search_by_keyword(
    query: str,
    top_k: int = 5,
) -> list[dict]:

    if not query.strip():
        return []

    collection = get_collection()

    # Get all indexed chunks.
    results = collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    documents = results.get(
        "documents",
        []
    )

    metadatas = results.get(
        "metadatas",
        []
    )

    ids = results.get(
        "ids",
        []
    )

    query_tokens = tokenize(query)

    search_results = []

    for index, document in enumerate(documents):

        score = calculate_keyword_score(
            query_tokens,
            document,
        )

        if score <= 0:
            continue

        search_results.append({
            "chunk_id": ids[index],
            "text": document,
            "metadata": metadatas[index],
            "keyword_score": score,
        })

    # Highest keyword score first.
    search_results.sort(
        key=lambda result: result["keyword_score"],
        reverse=True,
    )

    return search_results[:top_k]