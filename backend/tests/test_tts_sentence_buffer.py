import asyncio
from pathlib import Path

from app.services.tts.edge_tts_service import edge_tts_service


async def text_stream():
    chunks = [
        "Hello, ",
        "I am InterVox. ",
        "I can answer questions ",
        "from your uploaded ",
        "documents. ",
        "You can also ask ",
        "follow-up questions!",
    ]

    for chunk in chunks:
        print("TEXT CHUNK:", repr(chunk))
        yield chunk
        await asyncio.sleep(0.2)


async def main():
    print("=" * 60)
    print("INTERVOX SENTENCE-BUFFERED TTS TEST")
    print("=" * 60)

    output_path = Path(
        "tests/output_tts_sentence_buffer.mp3"
    )

    total_bytes = 0

    with output_path.open("wb") as audio_file:

        async for audio_chunk in edge_tts_service.stream(
            text_stream()
        ):
            print(
                "AUDIO CHUNK:",
                len(audio_chunk),
                "bytes"
            )

            audio_file.write(audio_chunk)
            total_bytes += len(audio_chunk)

    print("\nTotal audio bytes:", total_bytes)
    print("Audio saved to:", output_path)

    if total_bytes == 0:
        raise RuntimeError(
            "Sentence-buffered TTS returned no audio."
        )

    print("\n" + "=" * 60)
    print("SENTENCE-BUFFERED TTS TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())