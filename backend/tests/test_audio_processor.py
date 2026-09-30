import torch

from app.services.audio.processor import (
    TARGET_SAMPLE_RATE,
    audio_processor,
)


AUDIO_PATH = r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"


def main():

    print("=" * 60)
    print("INTERVOX AUDIO PROCESSOR TEST")
    print("=" * 60)

    print("\nLoading audio...")

    audio = audio_processor.load_audio(
        AUDIO_PATH
    )

    print("\nAudio loaded successfully.")

    print(
        f"Tensor type: {type(audio).__name__}"
    )

    print(
        f"Tensor dtype: {audio.dtype}"
    )

    print(
        f"Tensor shape: {audio.shape}"
    )

    duration = (
        audio.numel()
        / TARGET_SAMPLE_RATE
    )

    print(
        f"Sample rate: {TARGET_SAMPLE_RATE} Hz"
    )

    print(
        f"Duration: {duration:.2f} seconds"
    )

    print(
        f"Minimum value: {audio.min().item():.4f}"
    )

    print(
        f"Maximum value: {audio.max().item():.4f}"
    )

    assert isinstance(audio, torch.Tensor)

    assert audio.dtype == torch.float32

    assert audio.dim() == 1

    assert TARGET_SAMPLE_RATE == 16000

    assert audio.numel() > 0

    print("\n" + "=" * 60)
    print("AUDIO PROCESSOR TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()