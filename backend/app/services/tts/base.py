from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class TTSService(ABC):
    """
    Base interface for Text-to-Speech services.
    """

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """
        Convert text into audio bytes.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        text_stream: AsyncIterator[str]
    ) -> AsyncIterator[bytes]:
        """
        Convert a stream of text chunks into audio chunks.
        """
        raise NotImplementedError