# from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# from app.services.voice.turn_manager import turn_manager
# from app.services.voice.voice_response import voice_response_service


# router = APIRouter()


# @router.websocket("/ws/voice")
# async def voice_websocket(
#     websocket: WebSocket,
# ):
#     await websocket.accept()

#     try:
#         while True:
#             message = await websocket.receive_json()

#             message_type = message.get("type")

#             # --------------------------------------------------
#             # START VOICE TURN
#             # --------------------------------------------------

#             if message_type == "transcript":
#                 transcript = message.get(
#                     "text",
#                     "",
#                 )

#                 if not transcript.strip():
#                     await websocket.send_json(
#                         {
#                             "type": "error",
#                             "message": "Transcript cannot be empty.",
#                         }
#                     )
#                     continue

#                 # Cancel any previous active turn.
#                 await turn_manager.cancel_turn()

#                 # Create a new turn ID.
#                 current_turn_id = (
#                     await turn_manager.get_current_turn_id()
#                 )

#                 await websocket.send_json(
#                     {
#                         "type": "turn_started",
#                         "turn_id": current_turn_id,
#                     }
#                 )

#                 try:
#                     async for audio_chunk in (
#                         voice_response_service.stream_audio(
#                             transcript
#                         )
#                     ):
#                         # Do not send stale audio.
#                         if not await turn_manager.is_current(
#                             current_turn_id
#                         ):
#                             break

#                         if audio_chunk:
#                             await websocket.send_bytes(
#                                 audio_chunk
#                             )

#                 except Exception as exc:
#                     await websocket.send_json(
#                         {
#                             "type": "error",
#                             "message": str(exc),
#                         }
#                     )

#             # --------------------------------------------------
#             # INTERRUPT / BARGE-IN
#             # --------------------------------------------------

#             elif message_type == "interrupt":
#                 new_turn_id = (
#                     await turn_manager.cancel_turn()
#                 )

#                 await websocket.send_json(
#                     {
#                         "type": "turn_cancelled",
#                         "turn_id": new_turn_id,
#                     }
#                 )

#             # --------------------------------------------------
#             # PING
#             # --------------------------------------------------

#             elif message_type == "ping":
#                 await websocket.send_json(
#                     {
#                         "type": "pong",
#                     }
#                 )

#             else:
#                 await websocket.send_json(
#                     {
#                         "type": "error",
#                         "message": (
#                             f"Unknown message type: "
#                             f"{message_type}"
#                         ),
#                     }
#                 )

#     except WebSocketDisconnect:
#         await turn_manager.cancel_turn()

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.voice.turn_manager import turn_manager
from app.services.voice.voice_response import voice_response_service


router = APIRouter()


async def process_voice_turn(
    websocket: WebSocket,
    transcript: str,
    turn_id: int,
):
    """
    Process one voice turn.

    This runs as a separate asyncio task so that
    the WebSocket can continue receiving messages
    such as interrupt/barging-in events.
    """

    try:
        async for audio_chunk in (
            voice_response_service.stream_audio(
                transcript
            )
        ):
            # Stop immediately if this turn is stale.
            if not await turn_manager.is_current(
                turn_id
            ):
                break

            if audio_chunk:
                await websocket.send_bytes(
                    audio_chunk
                )

    except asyncio.CancelledError:
        print(
            f"Voice turn {turn_id} cancelled."
        )
        raise

    except Exception as exc:
        print(
            f"Voice turn {turn_id} failed:",
            exc,
        )


@router.websocket("/ws/voice")
async def voice_websocket(
    websocket: WebSocket,
):
    await websocket.accept()

    current_task: asyncio.Task | None = None

    try:
        while True:
            message = await websocket.receive_json()

            message_type = message.get("type")

            # --------------------------------------------------
            # NEW TRANSCRIPT / NEW TURN
            # --------------------------------------------------

            if message_type == "transcript":

                transcript = message.get(
                    "text",
                    "",
                )

                if not transcript.strip():
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": (
                                "Transcript cannot be empty."
                            ),
                        }
                    )
                    continue

                # Cancel previous voice task.
                if current_task is not None:
                    if not current_task.done():
                        current_task.cancel()

                        try:
                            await current_task
                        except asyncio.CancelledError:
                            pass

                # Invalidate previous turn.
                await turn_manager.cancel_turn()

                # Create a new turn ID.
                turn_id = (
                    await turn_manager.get_current_turn_id()
                ) + 1

                # Create dedicated voice task.
                current_task = asyncio.create_task(
                    process_voice_turn(
                        websocket=websocket,
                        transcript=transcript,
                        turn_id=turn_id,
                    )
                )

                # Register task with TurnManager.
                registered_turn_id = (
                    await turn_manager.start_turn(
                        task=current_task
                    )
                )

                await websocket.send_json(
                    {
                        "type": "turn_started",
                        "turn_id": registered_turn_id,
                    }
                )

            # --------------------------------------------------
            # USER INTERRUPTS AI
            # --------------------------------------------------

            elif message_type == "interrupt":

                print(
                    "\nUser interrupted current turn."
                )

                if current_task is not None:
                    if not current_task.done():
                        current_task.cancel()

                        try:
                            await current_task
                        except asyncio.CancelledError:
                            pass

                current_task = None

                cancelled_turn_id = (
                    await turn_manager.cancel_turn()
                )

                await websocket.send_json(
                    {
                        "type": "turn_cancelled",
                        "turn_id": cancelled_turn_id,
                    }
                )

            # --------------------------------------------------
            # PING
            # --------------------------------------------------

            elif message_type == "ping":

                await websocket.send_json(
                    {
                        "type": "pong"
                    }
                )

            # --------------------------------------------------
            # UNKNOWN MESSAGE
            # --------------------------------------------------

            else:

                await websocket.send_json(
                    {
                        "type": "error",
                        "message": (
                            f"Unknown message type: "
                            f"{message_type}"
                        ),
                    }
                )

    except WebSocketDisconnect:

        print(
            "Voice WebSocket disconnected."
        )

        if current_task is not None:
            if not current_task.done():
                current_task.cancel()

                try:
                    await current_task
                except asyncio.CancelledError:
                    pass

        await turn_manager.cancel_turn()