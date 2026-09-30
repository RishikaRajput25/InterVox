from app.services.stt.groq_stt import groq_stt_service


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"


def main():
    print("=" * 60)
    print("INTERVOX GROQ STT TEST")
    print("=" * 60)

    print("\nTranscribing audio with Groq Whisper...")

    transcript = groq_stt_service.transcribe(
        AUDIO_PATH
    )

    print("\n" + "=" * 60)
    print("TRANSCRIPT")
    print("=" * 60)

    print("\n", transcript)

    print("\n" + "=" * 60)
    print("Groq STT test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
    