import asyncio

from app.config.settings import settings
from google import genai


async def main():
    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    print("Checking Gemini async API...")

    print(
        "client.aio:",
        hasattr(client, "aio")
    )

    print(
        "client.aio.models:",
        hasattr(client.aio, "models")
    )

    print(
        "generate_content_stream:",
        hasattr(
            client.aio.models,
            "generate_content_stream"
        )
    )

    if not hasattr(
        client.aio.models,
        "generate_content_stream"
    ):
        print("\nAsync streaming API is NOT available.")
        return

    print("\nTesting async streaming...\n")

    response = await client.aio.models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents="Explain RAG in two short sentences.",
    )

    async for chunk in response:
        if chunk.text:
            print("ASYNC CHUNK:", repr(chunk.text))

    print("\nASYNC GEMINI STREAM TEST PASSED")


if __name__ == "__main__":
    asyncio.run(main())