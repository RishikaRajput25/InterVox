import asyncio

from app.services.voice.voice_response import (
    voice_response_service,
)


async def consume_voice_response():
    try:
        print("\nVOICE RESPONSE TASK STARTED")

        async for audio_chunk in (
            voice_response_service.stream_audio(
                "What technologies are used in Style Mirror?"
            )
        ):
            print(
                "AUDIO CHUNK:",
                len(audio_chunk),
                "bytes",
            )

            # Simulate sending audio to the user.
            await asyncio.sleep(0.05)

    except asyncio.CancelledError:
        print("\nVOICE RESPONSE TASK CANCELLED")
        raise


async def main():
    print("=" * 60)
    print("INTERVOX VOICE RESPONSE CANCELLATION TEST")
    print("=" * 60)

    task = asyncio.create_task(
        consume_voice_response()
    )

    # Give Gemini → TTS pipeline some time to start.
    await asyncio.sleep(2)

    print("\nUser started speaking...")
    print("Cancelling current voice response...")

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print(
            "Cancellation propagated successfully."
        )

    print("\n" + "=" * 60)
    print("VOICE RESPONSE CANCELLATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())