import time

from faster_whisper import WhisperModel

from app.services.stt.groq_stt import groq_stt_service


AUDIO_PATH = (
    r"C:\Users\ayush\Downloads"
    r"\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"
)


def benchmark_groq():
    print("\n" + "=" * 60)
    print("GROQ STT")
    print("=" * 60)

    start_time = time.perf_counter()

    transcript = groq_stt_service.transcribe(
        AUDIO_PATH
    )

    elapsed_time = (
        time.perf_counter() - start_time
    )

    print(f"\nTime: {elapsed_time:.2f} seconds")
    print(f"Transcript: {transcript}")

    return elapsed_time


def benchmark_local_whisper():
    print("\n" + "=" * 60)
    print("LOCAL FASTER-WHISPER")
    print("=" * 60)

    print("\nLoading local Whisper model...")

    load_start = time.perf_counter()

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",
    )

    load_time = (
        time.perf_counter() - load_start
    )

    print(
        f"Model load time: "
        f"{load_time:.2f} seconds"
    )

    print("\nTranscribing...")

    start_time = time.perf_counter()

    segments, info = model.transcribe(
        AUDIO_PATH,
        beam_size=5,
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    elapsed_time = (
        time.perf_counter() - start_time
    )

    print(
        f"Transcription time: "
        f"{elapsed_time:.2f} seconds"
    )

    print(f"Transcript: {transcript}")

    return elapsed_time


def main():
    print("=" * 60)
    print("INTERVOX STT PROVIDER BENCHMARK")
    print("=" * 60)

    groq_time = benchmark_groq()

    local_time = benchmark_local_whisper()

    print("\n" + "=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)

    print(f"\nGroq STT:            {groq_time:.2f} seconds")
    print(
        f"Local Faster-Whisper: "
        f"{local_time:.2f} seconds"
    )

    print("\nBenchmark completed.")


if __name__ == "__main__":
    main()