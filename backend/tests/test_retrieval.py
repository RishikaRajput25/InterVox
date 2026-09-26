from app.services.retrieval.semantic_search import search_documents


def main():

    query = "What is the main purpose of StyleMirror?"

    print("Query:")
    print(query)

    print("\nSearching...\n")

    results = search_documents(
        query=query,
        top_k=3,
    )

    for index, result in enumerate(results, start=1):

        print("=" * 70)

        print(f"Result {index}")

        print("\nDistance:")
        print(result["distance"])

        print("\nMetadata:")
        print(result["metadata"])

        print("\nText:")
        print(result["text"][:500])

    print("=" * 70)


if __name__ == "__main__":
    main()