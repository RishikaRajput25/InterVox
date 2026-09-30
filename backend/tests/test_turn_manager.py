import asyncio

from app.services.voice.turn_manager import turn_manager


async def test():
    turn1 = await turn_manager.start_turn()

    print("Turn 1:", turn1)
    print(
        "Turn 1 valid:",
        await turn_manager.is_current(turn1)
    )

    turn2 = await turn_manager.start_turn()

    print("Turn 2:", turn2)
    print(
        "Turn 1 valid after Turn 2:",
        await turn_manager.is_current(turn1)
    )
    print(
        "Turn 2 valid:",
        await turn_manager.is_current(turn2)
    )


if __name__ == "__main__":
    asyncio.run(test())