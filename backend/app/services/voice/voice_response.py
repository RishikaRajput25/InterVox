import asyncio
from collections.abc import AsyncIterator

from app.services.rag.rag_service import rag_service
from app.services.tts.edge_tts_service import edge_tts_service


class VoiceResponseService:
    """
    Connects the streaming RAG response to TTS.

    Pipeline:

    User transcript
        ↓
    RAG + Gemini streaming
        ↓
    Sentence buffering
        ↓
    Edge TTS
        ↓
    Audio chunks

    The complete pipeline is cancellable.
    If the current voice turn is cancelled,
    Gemini/RAG/TTS processing stops.
    """

    async def stream_audio(
        self,
        transcript: str,
    ) -> AsyncIterator[bytes]:
        """
        Generate streaming audio for a user transcript.

        Cancellation is allowed to propagate through
        the complete RAG → TTS pipeline.
        """

        if not transcript.strip():
            return

        text_stream = rag_service.ask_stream_async(
            query=transcript
        )

        try:
            async for audio_chunk in edge_tts_service.stream(
                text_stream
            ):
                if audio_chunk:
                    yield audio_chunk

        except asyncio.CancelledError:
            print(
                "Voice response pipeline cancelled."
            )
            raise


voice_response_service = VoiceResponseService()