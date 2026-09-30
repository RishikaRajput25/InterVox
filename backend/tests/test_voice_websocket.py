import asyncio

import websockets


async def main():
    uri = "ws://127.0.0.1:8000/ws/voice"

    print("=" * 60)
    print("INTERVOX WEBSOCKET VOICE TEST")
    print("=" * 60)

    async with websockets.connect(uri) as websocket:

        # --------------------------------------------------
        # 1. PING TEST
        # --------------------------------------------------

        print("\nSending ping...")

        await websocket.send(
            '{"type": "ping"}'
        )

        response = await websocket.recv()

        print(
            "Server response:",
            response,
        )

        # --------------------------------------------------
        # 2. START VOICE TURN
        # --------------------------------------------------

        print(
            "\nStarting voice turn..."
        )

        await websocket.send(
            '{"type": "transcript", '
            '"text": "What technologies are used in Style Mirror?"}'
        )

        response = await websocket.recv()

        print(
            "Server response:",
            response,
        )

        # --------------------------------------------------
        # 3. RECEIVE AUDIO
        # --------------------------------------------------

        print(
            "\nWaiting for audio chunks..."
        )

        audio_chunks = 0

        try:
            while audio_chunks < 5:

                message = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=15,
                )

                if isinstance(message, bytes):

                    audio_chunks += 1

                    print(
                        "AUDIO CHUNK:",
                        len(message),
                        "bytes",
                    )

                else:

                    print(
                        "TEXT:",
                        message,
                    )

        except asyncio.TimeoutError:

            print(
                "Timed out while waiting for audio."
            )

        # --------------------------------------------------
        # 4. INTERRUPT
        # --------------------------------------------------

        print(
            "\n🎤 USER INTERRUPTS AI"
        )

        await websocket.send(
            '{"type": "interrupt"}'
        )

        response = await websocket.recv()

        print(
            "Server response:",
            response,
        )

        # --------------------------------------------------
        # 5. START SECOND TURN
        # --------------------------------------------------

        print(
            "\nStarting second voice turn..."
        )

        await websocket.send(
            '{"type": "transcript", '
            '"text": "Which models can be used for virtual try on?"}'
        )

        response = await websocket.recv()

        print(
            "Server response:",
            response,
        )

        # --------------------------------------------------
        # 6. RECEIVE SECOND TURN AUDIO
        # --------------------------------------------------

        print(
            "\nWaiting for second turn audio..."
        )

        second_audio_chunks = 0

        try:
            while second_audio_chunks < 5:

                message = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=15,
                )

                if isinstance(message, bytes):

                    second_audio_chunks += 1

                    print(
                        "SECOND TURN AUDIO:",
                        len(message),
                        "bytes",
                    )

                else:

                    print(
                        "TEXT:",
                        message,
                    )

        except asyncio.TimeoutError:

            print(
                "Timed out while waiting for "
                "second turn audio."
            )

        # --------------------------------------------------
        # FINAL CHECK
        # --------------------------------------------------

        print("\n" + "-" * 60)
        print("FINAL CHECK")
        print("-" * 60)

        print(
            "First turn audio chunks:",
            audio_chunks,
        )

        print(
            "Second turn audio chunks:",
            second_audio_chunks,
        )

        if audio_chunks == 0:
            raise RuntimeError(
                "First turn produced no audio."
            )

        if second_audio_chunks == 0:
            raise RuntimeError(
                "Second turn produced no audio."
            )

        print("\n" + "=" * 60)
        print(
            "WEBSOCKET VOICE TEST PASSED"
        )
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())