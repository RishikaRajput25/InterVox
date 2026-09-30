from pathlib import Path

from faster_whisper import WhisperModel

from app.services.stt.base import STTService


MODEL_NAME = "base"


class LocalWhisperSTTService(STTService):

    def __init__(self):
        self.model = WhisperModel(
            MODEL_NAME,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(
        self,
        audio_path: str,
    ) -> str:

        file_path = Path(audio_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        segments, _ = self.model.transcribe(
            str(file_path),
            beam_size=5,
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        return transcript


local_whisper_stt_service = LocalWhisperSTTService()