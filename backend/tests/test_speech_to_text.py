from app.services.stt.groq_stt import (
    groq_stt_service,
)


AUDIO_PATH = "tests/output_speech.wav"


def main():

    print("=" * 60)
    print("INTERVOX SPEECH TO TEXT TEST")
    print("=" * 60)

    print("\nSending speech audio to Groq Whisper...")

    transcript = groq_stt_service.transcribe(
        AUDIO_PATH
    )

    print("\n" + "=" * 60)
    print("TRANSCRIPT")
    print("=" * 60)

    print(f"\n{transcript}")

    print("\n" + "=" * 60)
    print("SPEECH TO TEXT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()