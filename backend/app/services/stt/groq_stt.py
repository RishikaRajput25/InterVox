from pathlib import Path

from groq import Groq

from app.config.settings import settings
from app.services.stt.base import STTService


MODEL_NAME = "whisper-large-v3-turbo"


class GroqSTTService(STTService):

    def __init__(self):
        self.client = Groq(
            api_key=settings.groq_api_key
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

        with file_path.open("rb") as audio_file:

            transcription = (
                self.client.audio.transcriptions.create(
                    file=audio_file,
                    model=MODEL_NAME,
                    response_format="text",
                )
            )

        return transcription.strip()


groq_stt_service = GroqSTTService()