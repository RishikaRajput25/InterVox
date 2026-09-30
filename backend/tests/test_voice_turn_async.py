import asyncio

from app.services.voice.voice_turn import voice_turn_service


async def main():
    print("=" * 60)
    print("INTERVOX ASYNC VOICE TURN STREAM TEST")
    print("=" * 60)

    transcript = "What technologies are used in Style Mirror?"

    print("\nTranscript:")
    print(transcript)

    print("\nStreaming response:\n")

    async for chunk in voice_turn_service.stream_response(
        transcript
    ):
        print("CHUNK:", repr(chunk))

    print("\n" + "=" * 60)
    print("ASYNC VOICE TURN STREAM TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())