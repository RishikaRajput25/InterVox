
# import asyncio

# from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# from app.services.voice.turn_manager import turn_manager
# from app.services.voice.voice_response import voice_response_service


# router = APIRouter()


# async def process_voice_turn(
#     websocket: WebSocket,
#     transcript: str,
#     turn_id: int,
# ):
#     """
#     Process one voice turn.

#     This runs as a separate asyncio task so that
#     the WebSocket can continue receiving messages
#     such as interrupt/barging-in events.
#     """

#     try:
#         async for audio_chunk in (
#             voice_response_service.stream_audio(
#                 transcript
#             )
#         ):
#             # Stop immediately if this turn is stale.
#             if not await turn_manager.is_current(
#                 turn_id
#             ):
#                 break

#             if audio_chunk:
#                 await websocket.send_bytes(
#                     audio_chunk
#                 )

#     except asyncio.CancelledError:
#         print(
#             f"Voice turn {turn_id} cancelled."
#         )
#         raise

#     except Exception as exc:
#         print(
#             f"Voice turn {turn_id} failed:",
#             exc,
#         )


# @router.websocket("/ws/voice")
# async def voice_websocket(
#     websocket: WebSocket,
# ):
#     await websocket.accept()

#     current_task: asyncio.Task | None = None

#     try:
#         while True:
#             message = await websocket.receive_json()

#             message_type = message.get("type")

#             # --------------------------------------------------
#             # NEW TRANSCRIPT / NEW TURN
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
#                             "message": (
#                                 "Transcript cannot be empty."
#                             ),
#                         }
#                     )
#                     continue

#                 # Cancel previous voice task.
#                 if current_task is not None:
#                     if not current_task.done():
#                         current_task.cancel()

#                         try:
#                             await current_task
#                         except asyncio.CancelledError:
#                             pass

#                 # Invalidate previous turn.
#                 await turn_manager.cancel_turn()

#                 # Create a new turn ID.
#                 turn_id = (
#                     await turn_manager.get_current_turn_id()
#                 ) + 1

#                 # Create dedicated voice task.
#                 current_task = asyncio.create_task(
#                     process_voice_turn(
#                         websocket=websocket,
#                         transcript=transcript,
#                         turn_id=turn_id,
#                     )
#                 )

#                 # Register task with TurnManager.
#                 registered_turn_id = (
#                     await turn_manager.start_turn(
#                         task=current_task
#                     )
#                 )

#                 await websocket.send_json(
#                     {
#                         "type": "turn_started",
#                         "turn_id": registered_turn_id,
#                     }
#                 )

#             # --------------------------------------------------
#             # USER INTERRUPTS AI
#             # --------------------------------------------------

#             elif message_type == "interrupt":

#                 print(
#                     "\nUser interrupted current turn."
#                 )

#                 if current_task is not None:
#                     if not current_task.done():
#                         current_task.cancel()

#                         try:
#                             await current_task
#                         except asyncio.CancelledError:
#                             pass

#                 current_task = None

#                 cancelled_turn_id = (
#                     await turn_manager.cancel_turn()
#                 )

#                 await websocket.send_json(
#                     {
#                         "type": "turn_cancelled",
#                         "turn_id": cancelled_turn_id,
#                     }
#                 )

#             # --------------------------------------------------
#             # PING
#             # --------------------------------------------------

#             elif message_type == "ping":

#                 await websocket.send_json(
#                     {
#                         "type": "pong"
#                     }
#                 )

#             # --------------------------------------------------
#             # UNKNOWN MESSAGE
#             # --------------------------------------------------

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

#         print(
#             "Voice WebSocket disconnected."
#         )

#         if current_task is not None:
#             if not current_task.done():
#                 current_task.cancel()

#                 try:
#                     await current_task
#                 except asyncio.CancelledError:
#                     pass

#         await turn_manager.cancel_turn()

import asyncio
import json
import uuid
from pathlib import Path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.voice.turn_manager import turn_manager
from app.services.voice.voice_input import voice_input_service
from app.services.voice.voice_response import voice_response_service


router = APIRouter()


async def cancel_current_voice_task(
    current_task: asyncio.Task | None,
) -> None:
    if current_task is not None:
        if not current_task.done():
            current_task.cancel()

            try:
                await current_task
            except asyncio.CancelledError:
                pass


async def process_voice_turn(
    websocket: WebSocket,
    transcript: str,
    turn_id: int,
):
    """
    Process one transcript voice turn.

    RAG response is streamed into TTS and then
    sent to the WebSocket as binary audio chunks.
    """

    try:
        async for audio_chunk in (
            voice_response_service.stream_audio(
                transcript
            )
        ):
            # Ignore stale results.
            if not await turn_manager.is_current(
                turn_id
            ):
                break

            if audio_chunk:
                await websocket.send_bytes(
                    audio_chunk
                )

        # --------------------------------------------------
        # RESPONSE COMPLETE
        # --------------------------------------------------

        # Only send completion if this turn is
        # still the active turn.
        if await turn_manager.is_current(
            turn_id
        ):
            try:
                await websocket.send_json(
                    {
                        "type": "response_complete",
                        "turn_id": turn_id,
                    }
                )
            except WebSocketDisconnect:
                pass

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

        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "message": "Voice response failed.",
                }
            )
        except WebSocketDisconnect:
            pass


async def process_audio_turn(
    websocket: WebSocket,
    audio_bytes: bytes,
    turn_id: int,
):
    """
    Process recorded browser audio.

    Flow:

    Browser audio
        ↓
    temporary WebM file
        ↓
    VoiceInputService
        ↓
    VAD
        ↓
    Groq Whisper STT
        ↓
    transcript
        ↓
    RAG
        ↓
    TTS
        ↓
    binary audio chunks
    """

    input_path: Path | None = None
    output_path: Path | None = None

    try:
        audio_dir = Path("tests") / "voice_ws"

        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        input_path = (
            audio_dir
            / f"{uuid.uuid4()}.webm"
        )

        output_path = (
            audio_dir
            / f"{uuid.uuid4()}.wav"
        )

        # --------------------------------------------------
        # SAVE BROWSER AUDIO
        # --------------------------------------------------

        input_path.write_bytes(
            audio_bytes
        )

        # --------------------------------------------------
        # AUDIO → VAD → STT
        # --------------------------------------------------

        # VoiceInputService is synchronous,
        # so run it in a worker thread.
        transcript = await asyncio.to_thread(
            voice_input_service.process_audio,
            str(input_path),
            str(output_path),
        )

        # The turn may have been interrupted
        # while STT was running.
        if not await turn_manager.is_current(
            turn_id
        ):
            return

        if not transcript.strip():
            try:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "No speech detected.",
                    }
                )
            except WebSocketDisconnect:
                pass

            return

        # --------------------------------------------------
        # SEND TRANSCRIPT TO FRONTEND
        # --------------------------------------------------

        try:
            await websocket.send_json(
                {
                    "type": "transcript",
                    "turn_id": turn_id,
                    "text": transcript,
                }
            )
        except WebSocketDisconnect:
            return

        # --------------------------------------------------
        # RAG → TTS → AUDIO STREAM
        # --------------------------------------------------

        async for audio_chunk in (
            voice_response_service.stream_audio(
                transcript
            )
        ):
            # Ignore stale audio.
            if not await turn_manager.is_current(
                turn_id
            ):
                break

            if audio_chunk:
                try:
                    await websocket.send_bytes(
                        audio_chunk
                    )
                except WebSocketDisconnect:
                    return

        # --------------------------------------------------
        # RESPONSE COMPLETE
        # --------------------------------------------------

        # Only send completion if this turn is
        # still active.
        if await turn_manager.is_current(
            turn_id
        ):
            try:
                await websocket.send_json(
                    {
                        "type": "response_complete",
                        "turn_id": turn_id,
                    }
                )
            except WebSocketDisconnect:
                pass

    except asyncio.CancelledError:
        print(
            f"Audio voice turn {turn_id} cancelled."
        )
        raise

    except Exception as exc:
        print(
            f"Audio voice turn {turn_id} failed:",
            exc,
        )

        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "message": "Audio processing failed.",
                }
            )
        except WebSocketDisconnect:
            pass

    finally:
        # --------------------------------------------------
        # CLEAN TEMPORARY FILES
        # --------------------------------------------------

        if input_path is not None:
            try:
                input_path.unlink(
                    missing_ok=True
                )
            except Exception:
                pass

        if output_path is not None:
            try:
                output_path.unlink(
                    missing_ok=True
                )
            except Exception:
                pass


@router.websocket("/ws/voice")
async def voice_websocket(
    websocket: WebSocket,
):
    await websocket.accept()

    current_task: asyncio.Task | None = None

    # Audio received from the browser.
    audio_buffer = bytearray()

    try:
        while True:

            # --------------------------------------------------
            # RECEIVE MESSAGE
            # --------------------------------------------------

            try:
                message = await websocket.receive()

            except WebSocketDisconnect:
                print(
                    "Voice WebSocket disconnected."
                )
                break

            # --------------------------------------------------
            # BINARY AUDIO CHUNK
            # --------------------------------------------------

            if message.get("bytes") is not None:

                audio_chunk = message["bytes"]

                if audio_chunk:
                    audio_buffer.extend(
                        audio_chunk
                    )

                continue

            # --------------------------------------------------
            # DISCONNECT MESSAGE
            # --------------------------------------------------

            if message.get("type") == "websocket.disconnect":
                print(
                    "Voice WebSocket disconnected."
                )
                break

            # --------------------------------------------------
            # TEXT / JSON MESSAGE
            # --------------------------------------------------

            if message.get("text") is None:
                continue

            try:
                data = json.loads(
                    message["text"]
                )

            except json.JSONDecodeError:
                try:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "Invalid JSON message.",
                        }
                    )
                except WebSocketDisconnect:
                    break

                continue

            message_type = data.get(
                "type"
            )

            # ==================================================
            # AUDIO START
            # ==================================================

            if message_type == "audio_start":

                # A new speech attempt means the user
                # is taking control of the conversation.
                if current_task is not None:
                    await cancel_current_voice_task(
                        current_task
                    )

                current_task = None

                cancelled_turn_id = (
                    await turn_manager.cancel_turn()
                )

                audio_buffer.clear()

                try:
                    await websocket.send_json(
                        {
                            "type": "turn_cancelled",
                            "turn_id": cancelled_turn_id,
                        }
                    )
                except WebSocketDisconnect:
                    break

            # ==================================================
            # AUDIO END
            # ==================================================

            elif message_type == "audio_end":

                if not audio_buffer:

                    try:
                        await websocket.send_json(
                            {
                                "type": "error",
                                "message": "No audio received.",
                            }
                        )
                    except WebSocketDisconnect:
                        break

                    continue

                # Invalidate any previous turn.
                await turn_manager.cancel_turn()

                turn_id = (
                    await turn_manager.get_current_turn_id()
                ) + 1

                # Copy bytes before clearing the buffer.
                audio_bytes = bytes(
                    audio_buffer
                )

                audio_buffer.clear()

                # Create processing task.
                current_task = asyncio.create_task(
                    process_audio_turn(
                        websocket=websocket,
                        audio_bytes=audio_bytes,
                        turn_id=turn_id,
                    )
                )

                registered_turn_id = (
                    await turn_manager.start_turn(
                        task=current_task
                    )
                )

                try:
                    await websocket.send_json(
                        {
                            "type": "turn_started",
                            "turn_id": registered_turn_id,
                        }
                    )

                except WebSocketDisconnect:
                    await cancel_current_voice_task(
                        current_task
                    )

                    current_task = None
                    break

            # ==================================================
            # TRANSCRIPT TEST FLOW
            # ==================================================

            elif message_type == "transcript":

                transcript = data.get(
                    "text",
                    "",
                )

                if not transcript.strip():

                    try:
                        await websocket.send_json(
                            {
                                "type": "error",
                                "message": (
                                    "Transcript cannot be empty."
                                ),
                            }
                        )
                    except WebSocketDisconnect:
                        break

                    continue

                await cancel_current_voice_task(
                    current_task
                )

                current_task = None

                await turn_manager.cancel_turn()

                turn_id = (
                    await turn_manager.get_current_turn_id()
                ) + 1

                current_task = asyncio.create_task(
                    process_voice_turn(
                        websocket=websocket,
                        transcript=transcript,
                        turn_id=turn_id,
                    )
                )

                registered_turn_id = (
                    await turn_manager.start_turn(
                        task=current_task
                    )
                )

                try:
                    await websocket.send_json(
                        {
                            "type": "turn_started",
                            "turn_id": registered_turn_id,
                        }
                    )

                except WebSocketDisconnect:
                    await cancel_current_voice_task(
                        current_task
                    )

                    current_task = None
                    break

            # ==================================================
            # INTERRUPT
            # ==================================================

            elif message_type == "interrupt":

                print(
                    "\nUser interrupted current turn."
                )

                await cancel_current_voice_task(
                    current_task
                )

                current_task = None

                cancelled_turn_id = (
                    await turn_manager.cancel_turn()
                )

                audio_buffer.clear()

                try:
                    await websocket.send_json(
                        {
                            "type": "turn_cancelled",
                            "turn_id": cancelled_turn_id,
                        }
                    )
                except WebSocketDisconnect:
                    break

            # ==================================================
            # PING
            # ==================================================

            elif message_type == "ping":

                try:
                    await websocket.send_json(
                        {
                            "type": "pong"
                        }
                    )
                except WebSocketDisconnect:
                    break

            # ==================================================
            # UNKNOWN MESSAGE
            # ==================================================

            else:

                try:
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
                    break

    except WebSocketDisconnect:
        print(
            "Voice WebSocket disconnected."
        )

    finally:
        # --------------------------------------------------
        # CANCEL ACTIVE VOICE PROCESSING
        # --------------------------------------------------

        await cancel_current_voice_task(
            current_task
        )

        current_task = None

        # --------------------------------------------------
        # INVALIDATE CURRENT TURN
        # --------------------------------------------------

        await turn_manager.cancel_turn()

        # --------------------------------------------------
        # CLEAR BUFFERED AUDIO
        # --------------------------------------------------

        audio_buffer.clear()