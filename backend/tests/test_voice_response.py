import asyncio
from pathlib import Path

from app.services.voice.voice_response import (
    voice_response_service,
)


async def main():
    print("=" * 60)
    print("INTERVOX GEMINI → TTS END-TO-END TEST")
    print("=" * 60)

    transcript = (
        "What technologies are used in Style Mirror?"
    )

    print("\nUSER TRANSCRIPT:")
    print(transcript)

    output_path = Path(
        "tests/output_voice_response.mp3"
    )

    total_bytes = 0
    audio_chunks = 0

    print("\nStarting Gemini → TTS pipeline...\n")

    with output_path.open("wb") as audio_file:

        async for audio_chunk in (
            voice_response_service.stream_audio(
                transcript
            )
        ):
            audio_chunks += 1
            total_bytes += len(audio_chunk)

            print(
                f"AUDIO CHUNK {audio_chunks}: "
                f"{len(audio_chunk)} bytes"
            )

            audio_file.write(audio_chunk)

    print("\n" + "-" * 60)
    print("RESULT")
    print("-" * 60)

    print("Audio chunks:", audio_chunks)
    print("Total audio bytes:", total_bytes)
    print("Audio saved to:", output_path)

    if total_bytes == 0:
        raise RuntimeError(
            "End-to-end pipeline returned no audio."
        )

    print("\n" + "=" * 60)
    print("GEMINI → TTS END-TO-END TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())