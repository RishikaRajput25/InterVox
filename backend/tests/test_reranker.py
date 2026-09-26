from app.services.retrieval.hybrid_search import (
    search_hybrid,
)

from app.services.retrieval.reranker import (
    reranker,
)


def main():

    query = "What is the main purpose of StyleMirror?"

    print("User question:")
    print(query)

    print("\nRunning hybrid search...\n")

   
    hybrid_results = search_hybrid(
    query=query,
    top_k=10,
)

    print(
        "Hybrid candidates:",
        len(hybrid_results)
    )

    print("\nRunning reranker...\n")

    results = reranker.rerank(
        query=query,
        results=hybrid_results,
        top_k=5,
    )

    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result["metadata"]

        print(f"\nRESULT {index}")
        print("-" * 70)

        print(
            "Rerank Score:",
            round(
                result["rerank_score"],
                4
            )
        )

        print(
            "Hybrid Score:",
            round(
                result["hybrid_score"],
                4
            )
        )

        print(
            "Document:",
            metadata.get("filename")
        )

        print(
            "Page:",
            metadata.get("page_number")
        )

        print(
            "Text:",
            result["text"][:300]
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()