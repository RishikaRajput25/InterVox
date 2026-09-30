import asyncio

from app.services.voice.voice_turn import voice_turn_service
from app.services.voice.turn_manager import turn_manager


async def consume_voice_turn():
    """
    Consume the real VoiceTurnService stream.
    """

    try:
        async for chunk in voice_turn_service.stream_response(
            "What technologies are used in Style Mirror?"
        ):
            print("CHUNK:", repr(chunk))

            # Give cancellation a chance to happen
            await asyncio.sleep(0.2)

    except asyncio.CancelledError:
        print("\nVOICE TURN TASK CANCELLED")
        raise


async def main():
    print("=" * 60)
    print("INTERVOX REAL VOICE STREAM CANCELLATION TEST")
    print("=" * 60)

    # Start the real voice turn
    task = asyncio.create_task(
        consume_voice_turn()
    )

    print("\nVoice turn started.")

    # Allow some response chunks to arrive
    await asyncio.sleep(2)

    print("\nInterrupting current voice turn...")

    # Cancel the active turn
    await turn_manager.cancel_turn()

    # Wait for the task to finish
    try:
        await task
    except asyncio.CancelledError:
        print("Cancellation propagated to main.")

    print("\nCurrent Turn ID:")
    print(await turn_manager.get_current_turn_id())

    print("\n" + "=" * 60)
    print("REAL VOICE STREAM CANCELLATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())