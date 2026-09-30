import asyncio
from pathlib import Path

from app.services.tts.edge_tts_service import edge_tts_service


async def main():
    print("=" * 60)
    print("INTERVOX TTS TEST")
    print("=" * 60)

    text = "Hello, I am InterVox, your AI research assistant."

    print("\nText:")
    print(text)

    print("\nGenerating audio...")

    audio = await edge_tts_service.synthesize(text)

    print("Audio bytes:", len(audio))

    if not audio:
        raise RuntimeError("TTS returned empty audio.")

    output_path = Path("tests/output_tts.mp3")
    output_path.write_bytes(audio)

    print("\nAudio saved to:")
    print(output_path)

    print("\n" + "=" * 60)
    print("TTS TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())