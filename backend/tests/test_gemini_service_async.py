import asyncio

from app.services.llm.gemini import gemini_service


async def main():
    print("=" * 60)
    print("INTERVOX GEMINI SERVICE ASYNC STREAM TEST")
    print("=" * 60)

    prompt = "Explain RAG in two short sentences."

    print("\nStreaming:\n")

    async for chunk in gemini_service.stream_async(
        prompt
    ):
        print("CHUNK:", repr(chunk))

    print("\n" + "=" * 60)
    print("ASYNC GEMINI SERVICE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())