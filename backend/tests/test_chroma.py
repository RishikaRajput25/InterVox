from app.services.vectorstore.chroma import get_collection


def main():
    collection = get_collection()

    collection.add(
        ids=["test-chunk-1"],
        documents=[
            "InterVox is an AI research assistant."
        ],
        embeddings=[
            [0.1] * 384
        ],
        metadatas=[
            {
                "document_id": "test-document",
                "filename": "test.txt",
                "page_number": 1,
            }
        ],
    )

    print("Documents after insert:", collection.count())

    result = collection.get(
        ids=["test-chunk-1"]
    )

    print("\nRetrieved document:")
    print(result["documents"][0])

    print("\nRetrieved metadata:")
    print(result["metadatas"][0])


if __name__ == "__main__":
    main()