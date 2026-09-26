from app.services.retrieval.keyword_search import (
    search_by_keyword,
)


def main():

    query = "What is the main purpose of StyleMirror?"

    print("User question:")
    print(query)

    print("\nRunning keyword search...\n")

    results = search_by_keyword(
        query=query,
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
            "Score:",
            result["keyword_score"]
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

    print("=" * 70)


if __name__ == "__main__":
    main()