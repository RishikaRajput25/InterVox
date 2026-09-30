import torch

from silero_vad import (
    get_speech_timestamps,
    load_silero_vad,
)


TARGET_SAMPLE_RATE = 16000


class VADService:

    def __init__(self):
        self.model = load_silero_vad()

    def detect_speech(
        self,
        audio: torch.Tensor,
    ) -> list[dict]:

        if audio.numel() == 0:
            return []

        return get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=TARGET_SAMPLE_RATE,
        )

    def extract_speech(
        self,
        audio: torch.Tensor,
    ) -> list[torch.Tensor]:

        speech_segments = self.detect_speech(audio)

        extracted_segments = []

        for segment in speech_segments:
            start = segment["start"]
            end = segment["end"]

            speech_audio = audio[start:end]

            extracted_segments.append(
                speech_audio
            )

        return extracted_segments


vad_service = VADService()