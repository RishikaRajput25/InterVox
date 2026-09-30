from app.services.voice.voice_input import (
    voice_input_service,
)


AUDIO_PATH = (
    r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"
)


def main():

    print("=" * 60)
    print("INTERVOX VOICE INPUT SERVICE TEST")
    print("=" * 60)

    print("\nProcessing voice input...")

    transcript = (
        voice_input_service.process_audio(
            AUDIO_PATH
        )
    )

    print("\n" + "=" * 60)
    print("FINAL TRANSCRIPT")
    print("=" * 60)

    print(f"\n{transcript}")

    print("\n" + "=" * 60)
    print("VOICE INPUT SERVICE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()