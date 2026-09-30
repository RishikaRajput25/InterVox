import av
import torch

from app.services.voice.vad import (
    TARGET_SAMPLE_RATE,
    vad_service,
)


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"


def load_audio_with_pyav(
    audio_path: str,
    sample_rate: int = TARGET_SAMPLE_RATE,
) -> torch.Tensor:

    container = av.open(audio_path)

    try:
        audio_stream = container.streams.audio[0]

        resampler = av.audio.resampler.AudioResampler(
            format="s16",
            layout="mono",
            rate=sample_rate,
        )

        audio_samples = []

        for frame in container.decode(audio_stream):
            resampled_frames = resampler.resample(frame)

            for resampled_frame in resampled_frames:
                array = resampled_frame.to_ndarray()

                audio_samples.append(
                    torch.from_numpy(array)
                )

        if not audio_samples:
            raise ValueError("No audio samples found.")

        audio = torch.cat(
            audio_samples,
            dim=1,
        )

        audio = audio.squeeze(0)
        audio = audio.float() / 32768.0

        return audio

    finally:
        container.close()


def main():

    print("=" * 60)
    print("INTERVOX VAD SERVICE TEST")
    print("=" * 60)

    print("\nLoading audio...")

    audio = load_audio_with_pyav(
        AUDIO_PATH
    )

    duration = (
        len(audio) / TARGET_SAMPLE_RATE
    )

    print(
        f"Audio duration: {duration:.2f} seconds"
    )

    print("\nRunning VADService...")

    speech_segments = vad_service.detect_speech(
        audio
    )

    print("\n" + "=" * 60)
    print("VAD RESULT")
    print("=" * 60)

    if not speech_segments:
        print("\nNo speech detected.")
        return

    print(
        f"\nSpeech segments detected: "
        f"{len(speech_segments)}"
    )

    total_speech_samples = 0

    for index, segment in enumerate(
        speech_segments,
        start=1,
    ):

        start = segment["start"]
        end = segment["end"]

        segment_duration = (
            end - start
        ) / TARGET_SAMPLE_RATE

        total_speech_samples += (
            end - start
        )

        print(f"\nSegment {index}:")
        print(
            f"Start: "
            f"{start / TARGET_SAMPLE_RATE:.2f}s"
        )
        print(
            f"End: "
            f"{end / TARGET_SAMPLE_RATE:.2f}s"
        )
        print(
            f"Duration: "
            f"{segment_duration:.2f}s"
        )

    total_speech_duration = (
        total_speech_samples
        / TARGET_SAMPLE_RATE
    )

    print(
        f"\nTotal detected speech: "
        f"{total_speech_duration:.2f}s"
    )

    print("\nVAD service test completed successfully.")


if __name__ == "__main__":
    main()
    