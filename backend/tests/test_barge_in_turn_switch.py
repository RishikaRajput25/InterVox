import asyncio

from app.services.voice.turn_manager import turn_manager
from app.services.voice.voice_response import (
    voice_response_service,
)


async def run_voice_turn(
    turn_id: int,
    transcript: str,
):
    try:
        print(
            f"\nTURN {turn_id} STARTED"
        )

        async for audio_chunk in (
            voice_response_service.stream_audio(
                transcript
            )
        ):
            # Never allow stale turns to produce audio.
            if not await turn_manager.is_current(
                turn_id
            ):
                print(
                    f"TURN {turn_id} AUDIO BLOCKED "
                    "(stale turn)"
                )
                break

            print(
                f"TURN {turn_id} AUDIO:",
                len(audio_chunk),
                "bytes",
            )

            # Simulate sending audio to browser.
            await asyncio.sleep(0.05)

    except asyncio.CancelledError:
        print(
            f"TURN {turn_id} CANCELLED"
        )
        raise


async def start_voice_turn(
    transcript: str,
):
    # Reserve the next turn ID.
    next_turn_id = (
        await turn_manager.get_current_turn_id()
    ) + 1

    # Create the actual voice task.
    task = asyncio.create_task(
        run_voice_turn(
            next_turn_id,
            transcript,
        )
    )

    # Register this task with TurnManager.
    turn_id = await turn_manager.start_turn(
        task=task
    )

    return turn_id, task


async def main():
    print("=" * 60)
    print("INTERVOX BARGE-IN TURN SWITCH TEST")
    print("=" * 60)

    # --------------------------------------------------
    # TURN 1
    # --------------------------------------------------

    turn1_id, turn1_task = (
        await start_voice_turn(
            "What technologies are used in Style Mirror?"
        )
    )

    print(
        f"\nActive Turn: {turn1_id}"
    )

    # Let Turn 1 start generating audio.
    await asyncio.sleep(2)

    # --------------------------------------------------
    # USER INTERRUPTS
    # --------------------------------------------------

    print(
        "\n🎤 USER INTERRUPTS TURN 1"
    )

    await turn_manager.cancel_turn()

    try:
        await turn1_task
    except asyncio.CancelledError:
        pass

    print(
        "\nTurn 1 successfully stopped."
    )

    # --------------------------------------------------
    # TURN 2
    # --------------------------------------------------

    print(
        "\nStarting Turn 2..."
    )

    turn2_id, turn2_task = (
        await start_voice_turn(
            "What models can be used for virtual try on?"
        )
    )

    print(
        f"Active Turn: {turn2_id}"
    )

    # Let Turn 2 generate some audio.
    await asyncio.sleep(4)

    # Stop Turn 2 cleanly.
    print(
        "\nStopping Turn 2..."
    )

    await turn_manager.cancel_turn()

    try:
        await turn2_task
    except asyncio.CancelledError:
        pass

    # --------------------------------------------------
    # FINAL CHECK
    # --------------------------------------------------

    current_turn_id = (
        await turn_manager.get_current_turn_id()
    )

    turn1_valid = (
        await turn_manager.is_current(
            turn1_id
        )
    )

    turn2_valid = (
        await turn_manager.is_current(
            turn2_id
        )
    )

    print("\n" + "-" * 60)
    print("FINAL STATE")
    print("-" * 60)

    print(
        "Current Turn ID:",
        current_turn_id,
    )

    print(
        "Turn 1 valid:",
        turn1_valid,
    )

    print(
        "Turn 2 valid:",
        turn2_valid,
    )

    if turn1_valid:
        raise RuntimeError(
            "ERROR: Turn 1 is still valid!"
        )

    if turn2_valid:
        raise RuntimeError(
            "ERROR: Turn 2 should have been cancelled!"
        )

    print("\n" + "=" * 60)
    print(
        "BARGE-IN TURN SWITCH TEST PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())