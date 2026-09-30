# import asyncio
# import json

# import websockets


# async def test_voice_websocket():
#     uri = "ws://127.0.0.1:8000/ws/voice"

#     async with websockets.connect(uri) as websocket:

#         # 1. Ping test
#         await websocket.send(
#             json.dumps({
#                 "type": "ping"
#             })
#         )

#         message = await websocket.recv()
#         print("PING RESPONSE:", message)

#         # 2. Transcript test
#         await websocket.send(
#             json.dumps({
#                 "type": "transcript",
#                 "text": "What technologies are used in StyleMirror?"
#             })
#         )

#         # 3. Receive responses
#         while True:
#             message = await websocket.recv()

#             if isinstance(message, bytes):
#                 print(
#                     "RECEIVED BINARY AUDIO:",
#                     len(message),
#                     "bytes"
#                 )
#             else:
#                 print(
#                     "RECEIVED JSON:",
#                     message
#                 )

#                 data = json.loads(message)

#                 if data.get("type") == "error":
#                     break


# asyncio.run(test_voice_websocket())

import asyncio
import json
import websockets


async def test_barge_in():
    uri = "ws://127.0.0.1:8000/ws/voice"

    async with websockets.connect(
        uri,
        open_timeout=30,
        ping_interval=None,
    ) as websocket:

        print("CONNECTED")

        # -----------------------------
        # TURN 1
        # -----------------------------

        await websocket.send(json.dumps({
            "type": "transcript",
            "text": "What technologies are used in StyleMirror?"
        }))

        print("TURN 1 SENT")

        # Wait for first audio
        while True:
            message = await websocket.recv()

            if isinstance(message, bytes):
                print("TURN 1 AUDIO:", len(message))

                # Interrupt turn 1
                await websocket.send(json.dumps({
                    "type": "interrupt"
                }))

                print("INTERRUPT SENT")
                break

            print("TURN 1 JSON:", message)

        # Wait for cancellation
        while True:
            message = await websocket.recv()

            if isinstance(message, bytes):
                print("OLD AUDIO AFTER INTERRUPT:", len(message))
                continue

            print("AFTER INTERRUPT:", message)

            data = json.loads(message)

            if data.get("type") == "turn_cancelled":
                print("TURN 1 CANCELLED")
                break

        # -----------------------------
        # TURN 2
        # -----------------------------

        await websocket.send(json.dumps({
            "type": "transcript",
            "text": "What is the main purpose of this project?"
        }))

        print("TURN 2 SENT")

        # Wait for turn 2 completion
        while True:
            message = await websocket.recv()

            if isinstance(message, bytes):
                print("TURN 2 AUDIO:", len(message))
                continue

            print("TURN 2 JSON:", message)

            data = json.loads(message)

            if data.get("type") == "response_complete":
                print("TURN 2 COMPLETED")
                break


asyncio.run(test_barge_in())