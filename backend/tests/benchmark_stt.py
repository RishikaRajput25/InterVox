import time

from faster_whisper import WhisperModel


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.42.29 PM.mp4"

MODEL_NAME = "base"


def main():
    print("=" * 60)
    print("INTERVOX STT LATENCY TEST")
    print("=" * 60)

    print(f"\nModel: {MODEL_NAME}")
    print("Device: CPU")
    print("Compute type: int8")

    # -----------------------------
    # 1. Model loading time
    # -----------------------------
    print("\nLoading model...")

    load_start = time.perf_counter()

    model = WhisperModel(
        MODEL_NAME,
        device="cpu",
        compute_type="int8",
    )

    load_time = time.perf_counter() - load_start

    print(f"Model loaded in: {load_time:.2f} seconds")

    # -----------------------------
    # 2. Transcription time
    # -----------------------------
    print("\nTranscribing audio...")

    transcription_start = time.perf_counter()

    segments, info = model.transcribe(
        AUDIO_PATH,
        beam_size=5,
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    transcription_time = (
        time.perf_counter() - transcription_start
    )

    # -----------------------------
    # 3. Results
    # -----------------------------
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)

    print(f"\nLanguage: {info.language}")
    print(
        f"Language probability: "
        f"{info.language_probability:.2f}"
    )

    print(
        f"\nTranscription time: "
        f"{transcription_time:.2f} seconds"
    )

    print("\nTranscript:")
    print(transcript)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()