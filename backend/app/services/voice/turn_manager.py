import asyncio


class TurnManager:
    """
    Manages the currently active voice turn.

    Each new voice turn gets a unique sequential turn ID.

    Cancelling a turn invalidates the current turn but does
    not consume a new turn ID. This keeps logical turn IDs
    sequential while still preventing stale results.
    """

    def __init__(self):
        self._current_turn_id = 0
        self._valid_turn_id: int | None = None
        self._current_task: asyncio.Task | None = None

    async def start_turn(
        self,
        task: asyncio.Task | None = None,
    ) -> int:
        """
        Start a new voice turn.

        The previous turn is cancelled and invalidated.
        A new sequential turn ID is generated.
        """

        # Invalidate/cancel any previous turn.
        if self._current_task is not None:
            if not self._current_task.done():
                self._current_task.cancel()

        # Generate the next logical turn ID.
        self._current_turn_id += 1

        # This turn is now valid/current.
        self._valid_turn_id = self._current_turn_id

        self._current_task = task

        return self._current_turn_id

    async def cancel_turn(self) -> int:
        """
        Cancel the currently active turn.

        The cancelled turn ID is returned, but a new ID is
        NOT generated because no new logical turn has started.
        """

        cancelled_turn_id = self._current_turn_id

        # Invalidate the current turn immediately.
        self._valid_turn_id = None

        # Cancel the active task.
        if self._current_task is not None:
            if not self._current_task.done():
                self._current_task.cancel()

        self._current_task = None

        return cancelled_turn_id

    async def is_current(
        self,
        turn_id: int,
    ) -> bool:
        """
        Check whether the given turn is still valid/current.
        """

        return turn_id == self._valid_turn_id

    async def get_current_turn_id(self) -> int:
        """
        Return the latest logical turn ID.
        """

        return self._current_turn_id


turn_manager = TurnManager()