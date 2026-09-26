from faster_whisper import WhisperModel


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"


def main():
    print("Loading Whisper tiny model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
    )

    print("Model loaded.")
    print("Transcribing audio...\n")

    segments, info = model.transcribe(
        AUDIO_PATH,
        beam_size=5,
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    print("Detected language:", info.language)
    print("Language probability:", info.language_probability)

    print("\nTRANSCRIPT:")
    print(transcript)


if __name__ == "__main__":
    main()