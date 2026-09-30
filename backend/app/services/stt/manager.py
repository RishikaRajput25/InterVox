from app.services.stt.groq_stt import (
    groq_stt_service,
)
from app.services.stt.local_whisper import (
    local_whisper_stt_service,
)


class STTManager:

    def transcribe(
        self,
        audio_path: str,
    ) -> str:

        try:
            return groq_stt_service.transcribe(
                audio_path
            )

        except Exception as groq_error:
            print(
                "Groq STT failed. "
                "Falling back to local Whisper."
            )
            print(
                f"Groq error: {groq_error}"
            )

            return local_whisper_stt_service.transcribe(
                audio_path
            )


stt_manager = STTManager()