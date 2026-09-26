from app.services.llm.gemini import gemini_service


def main():
    prompt = "Explain RAG in simple terms in 3 sentences."

    print("Sending request to Gemini...\n")

    response = gemini_service.generate(prompt)

    print("Gemini response:")
    print(response)


if __name__ == "__main__":
    main()