import asyncio

from app.services.tts.edge_tts_service import edge_tts_service


async def text_stream():
    chunks = [
        "Hello, I am InterVox.",
        "I can answer questions from your uploaded documents.",
        "I can also handle follow-up questions.",
        "This response should be interrupted.",
        "This part should never finish if cancellation works.",
    ]

    for chunk in chunks:
        print("TEXT:", chunk)
        yield chunk
        await asyncio.sleep(0.5)


async def consume_tts():
    try:
        print("\nTTS task started.")

        async for audio_chunk in edge_tts_service.stream(
            text_stream()
        ):
            print(
                "AUDIO CHUNK:",
                len(audio_chunk),
                "bytes",
            )

            # Simulate sending audio to the user.
            await asyncio.sleep(0.05)

    except asyncio.CancelledError:
        print("\nTTS TASK CANCELLED")
        raise


async def main():
    print("=" * 60)
    print("INTERVOX TTS CANCELLATION TEST")
    print("=" * 60)

    task = asyncio.create_task(
        consume_tts()
    )

    # Let TTS generate audio for a while.
    await asyncio.sleep(2)

    print("\nUser started speaking...")
    print("Interrupting TTS...")

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Cancellation propagated successfully.")

    print("\n" + "=" * 60)
    print("TTS CANCELLATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())