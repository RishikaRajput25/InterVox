# from app.services.rag.rag_service import rag_service


# def main():

#     query = "What is the main purpose of StyleMirror?"

#     print("User question:")
#     print(query)

#     print("\nRunning RAG...\n")

#     result = rag_service.ask(
#         query=query,
#         top_k=5,
#     )

#     print("=" * 70)

#     print("ANSWER:")
#     print(result["answer"])

#     print("\nSOURCES:")

#     for source in result["sources"]:
#         print(
#             f"- {source['filename']} "
#             f"(Page {source['page_number']})"
#         )

#     print("=" * 70)


# if __name__ == "__main__":
#     main()

from app.services.rag.rag_service import rag_service


QUESTIONS = [
    "What technical skills are mentioned in the resume?",
    "What is the main purpose of StyleMirror?",
    "What AI-related technologies are mentioned across the available documents?",
]


def run_question(query: str):

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(query)

    print("\nRunning RAG...\n")

    result = rag_service.ask(
        query=query,
        top_k=5,
    )

    print("ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['filename']} "
            f"(Page {source['page_number']})"
        )

    print("=" * 70)


def main():

    for question in QUESTIONS:
        run_question(question)


if __name__ == "__main__":
    main()