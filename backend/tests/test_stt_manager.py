from app.services.stt.manager import stt_manager


AUDIO_PATH = (
    r"C:\Users\ayush\Downloads"
    r"\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"
)


def main():
    print("=" * 60)
    print("INTERVOX STT MANAGER TEST")
    print("=" * 60)

    print("\nTranscribing through STT Manager...")

    transcript = stt_manager.transcribe(
        AUDIO_PATH
    )

    print("\n" + "=" * 60)
    print("FINAL TRANSCRIPT")
    print("=" * 60)

    print(f"\n{transcript}")

    print("\n" + "=" * 60)
    print("STT Manager test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()