
# import asyncio
# from collections.abc import AsyncIterator

# from app.services.rag.rag_service import rag_service
# from app.services.voice.turn_manager import turn_manager


# class VoiceTurnService:

#     async def stream_response(
#         self,
#         transcript: str,
#     ) -> AsyncIterator[str]:
#         """
#         Start a new voice turn and stream the RAG response
#         asynchronously.

#         If the turn becomes invalid because the user interrupts,
#         remaining chunks are discarded.
#         """

#         if not transcript.strip():
#             return

#         # Start a new turn
#         turn_id = await turn_manager.start_turn()

#         try:
#             # Stream the RAG response asynchronously
#             async for chunk in rag_service.ask_stream_async(
#                 query=transcript
#             ):
#                 # Stop processing if this turn is no longer current
#                 if not await turn_manager.is_current(turn_id):
#                     break

#                 if chunk:
#                     yield chunk

#         except asyncio.CancelledError:
#             # Current generation was explicitly cancelled
#             raise


# voice_turn_service = VoiceTurnService()

import asyncio
from collections.abc import AsyncIterator

from app.services.rag.rag_service import rag_service
from app.services.voice.turn_manager import turn_manager


class VoiceTurnService:

    async def stream_response(
        self,
        transcript: str,
    ) -> AsyncIterator[str]:
        """
        Start a voice turn and stream the RAG response.

        The current turn can be cancelled by TurnManager.
        """

        if not transcript.strip():
            return

        # Start a new turn
        turn_id = await turn_manager.start_turn()

        try:
            async for chunk in rag_service.ask_stream_async(
                query=transcript
            ):
                # Ignore stale chunks
                if not await turn_manager.is_current(turn_id):
                    break

                if chunk:
                    yield chunk

        except asyncio.CancelledError:
            # The active voice turn was cancelled.
            print(
                f"Voice turn {turn_id} cancelled."
            )
            raise


voice_turn_service = VoiceTurnService()