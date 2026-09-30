from pathlib import Path

from app.services.audio.processor import (
    audio_processor,
)
from app.services.voice.vad import (
    vad_service,
)


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"

OUTPUT_PATH = (
    "tests/output_speech.wav"
)


def main():

    print("=" * 60)
    print("INTERVOX SPEECH AUDIO EXPORT TEST")
    print("=" * 60)

    print("\nLoading audio...")

    audio = audio_processor.load_audio(
        AUDIO_PATH
    )

    print(
        f"Original audio: "
        f"{audio.numel() / 16000:.2f}s"
    )

    print("\nDetecting speech...")

    speech_segments = (
        vad_service.extract_speech(
            audio
        )
    )

    if not speech_segments:
        raise ValueError(
            "No speech detected."
        )

    print(
        f"Speech segments: "
        f"{len(speech_segments)}"
    )

    speech_audio = speech_segments[0]

    print(
        f"Speech duration: "
        f"{speech_audio.numel() / 16000:.2f}s"
    )

    print("\nSaving WAV...")

    audio_processor.save_wav(
        speech_audio,
        OUTPUT_PATH,
    )

    output_file = Path(
        OUTPUT_PATH
    )

    print(
        f"Saved: {output_file}"
    )

    print(
        f"File exists: "
        f"{output_file.exists()}"
    )

    print(
        f"File size: "
        f"{output_file.stat().st_size} bytes"
    )

    print("\n" + "=" * 60)
    print("AUDIO EXPORT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()