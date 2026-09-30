import io
from collections.abc import AsyncIterator

import edge_tts

from app.services.tts.base import TTSService
from app.services.tts.text_cleaner import clean_text_for_tts


class EdgeTTSService(TTSService):
    """
    Microsoft Edge online TTS implementation.
    """

    def __init__(
        self,
        voice: str = "en-US-AriaNeural",
    ):
        self.voice = voice

    async def synthesize(
        self,
        text: str,
    ) -> bytes:
        """
        Convert complete text into MP3 audio bytes.
        """

        text = clean_text_for_tts(text)

        if not text:
            return b""

        communicate = edge_tts.Communicate(
            text,
            self.voice,
        )

        audio_buffer = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(
                    chunk["data"]
                )

        return audio_buffer.getvalue()

    async def _synthesize_chunk(
        self,
        text: str,
    ) -> AsyncIterator[bytes]:
        """
        Convert one complete phrase/sentence
        into audio chunks.
        """

        text = clean_text_for_tts(text)

        if not text:
            return

        communicate = edge_tts.Communicate(
            text,
            self.voice,
        )

        async for chunk in communicate.stream():

            if chunk["type"] == "audio":
                yield chunk["data"]

    async def stream(
        self,
        text_stream: AsyncIterator[str],
    ) -> AsyncIterator[bytes]:
        """
        Convert streaming LLM text into speech.

        Markdown is cleaned before TTS.
        Text is buffered until a sentence-ending
        punctuation mark is received.
        """

        buffer = ""

        sentence_endings = (
            ".",
            "?",
            "!",
        )

        async for text in text_stream:

            if not text:
                continue

            # Clean Markdown from the incoming
            # Gemini response chunk.
            cleaned_text = clean_text_for_tts(
                text
            )

            if not cleaned_text:
                continue

            buffer += cleaned_text

            # Process complete sentences.
            while True:

                sentence_end = -1

                for index, character in enumerate(
                    buffer
                ):
                    if character in sentence_endings:
                        sentence_end = index
                        break

                if sentence_end == -1:
                    break

                sentence = buffer[
                    : sentence_end + 1
                ]

                buffer = buffer[
                    sentence_end + 1 :
                ]

                async for audio_chunk in (
                    self._synthesize_chunk(
                        sentence
                    )
                ):
                    yield audio_chunk

        # Process remaining text.
        if buffer.strip():

            async for audio_chunk in (
                self._synthesize_chunk(
                    buffer
                )
            ):
                yield audio_chunk


edge_tts_service = EdgeTTSService()