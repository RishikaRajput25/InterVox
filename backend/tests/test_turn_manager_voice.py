import asyncio

from app.services.voice.turn_manager import turn_manager
from app.services.voice.voice_response import (
    voice_response_service,
)


async def voice_turn_task(
    turn_id: int,
):
    try:
        print(f"\nTURN {turn_id} TASK STARTED")

        async for audio_chunk in (
            voice_response_service.stream_audio(
                "What technologies are used in Style Mirror?"
            )
        ):
            if not await turn_manager.is_current(
                turn_id
            ):
                print(
                    f"TURN {turn_id} became stale."
                )
                break

            print(
                f"TURN {turn_id} AUDIO:",
                len(audio_chunk),
                "bytes",
            )

            # Simulate sending audio to user.
            await asyncio.sleep(0.05)

    except asyncio.CancelledError:
        print(
            f"\nTURN {turn_id} TASK CANCELLED"
        )
        raise


async def main():
    print("=" * 60)
    print("INTERVOX TURN MANAGER + VOICE TEST")
    print("=" * 60)

    # Create the actual voice task first.
    task = asyncio.create_task(
        voice_turn_task(
            turn_manager._current_turn_id + 1
        )
    )

    # Register this task with TurnManager.
    turn_id = await turn_manager.start_turn(
        task=task
    )

    print(
        f"\nStarted Turn ID: {turn_id}"
    )

    # Give the pipeline time to start.
    await asyncio.sleep(2)

    print(
        "\nUser started speaking..."
    )

    print(
        "Cancelling current turn..."
    )

    await turn_manager.cancel_turn()

    try:
        await task
    except asyncio.CancelledError:
        print(
            "Cancellation reached main task."
        )

    current_turn_id = (
        await turn_manager.get_current_turn_id()
    )

    is_old_turn_current = (
        await turn_manager.is_current(
            turn_id
        )
    )

    print(
        "\nCurrent Turn ID:",
        current_turn_id
    )

    print(
        "Old Turn still valid:",
        is_old_turn_current
    )

    if is_old_turn_current:
        raise RuntimeError(
            "Old turn is still valid!"
        )

    print("\n" + "=" * 60)
    print(
        "TURN MANAGER + VOICE CANCELLATION TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
