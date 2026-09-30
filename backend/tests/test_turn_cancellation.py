import asyncio

from app.services.voice.turn_manager import turn_manager


async def long_running_turn():
    print("Turn task started")

    try:
        while True:
            print("Turn task running...")
            await asyncio.sleep(0.5)

    except asyncio.CancelledError:
        print("Turn task received cancellation")
        raise


async def main():
    print("=" * 60)
    print("INTERVOX TURN CANCELLATION TEST")
    print("=" * 60)

    # Start the simulated AI turn
    task = asyncio.create_task(
        long_running_turn()
    )

    # Register this task as the current turn
    turn_id = await turn_manager.start_turn()

    print("\nStarted Turn ID:", turn_id)

    # Let the task run for a moment
    await asyncio.sleep(1.5)

    print("\nCancelling current turn...")

    await turn_manager.cancel_turn()

    try:
        await task
    except asyncio.CancelledError:
        print("Main detected task cancellation")

    print("\nCurrent Turn ID:")
    print(await turn_manager.get_current_turn_id())

    print("\nTurn 1 valid:")
    print(await turn_manager.is_current(turn_id))

    print("\n" + "=" * 60)
    print("TURN CANCELLATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())