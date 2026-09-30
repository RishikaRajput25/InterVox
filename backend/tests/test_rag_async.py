import asyncio

from app.services.rag.rag_service import rag_service


async def main():
    print("=" * 60)
    print("INTERVOX ASYNC RAG STREAM TEST")
    print("=" * 60)

    query = "What technologies are used in Style Mirror?"

    print("\nQuery:")
    print(query)

    print("\nStreaming response:\n")

    async for chunk in rag_service.ask_stream_async(
        query
    ):
        print("CHUNK:", repr(chunk))

    print("\n" + "=" * 60)
    print("ASYNC RAG STREAM TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())