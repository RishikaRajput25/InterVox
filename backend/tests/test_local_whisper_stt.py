from app.services.stt.local_whisper import (
    local_whisper_stt_service,
)


AUDIO_PATH = (
    r"C:\Users\ayush\Downloads"
    r"\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"
)


def main():
    print("=" * 60)
    print("INTERVOX LOCAL WHISPER STT TEST")
    print("=" * 60)

    print("\nTranscribing with local Faster-Whisper...")

    transcript = local_whisper_stt_service.transcribe(
        AUDIO_PATH
    )

    print("\n" + "=" * 60)
    print("TRANSCRIPT")
    print("=" * 60)

    print(f"\n{transcript}")

    print("\n" + "=" * 60)
    print("Local Whisper STT test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()