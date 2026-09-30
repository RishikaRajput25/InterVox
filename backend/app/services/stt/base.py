from abc import ABC, abstractmethod


class STTService(ABC):

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
    ) -> str:
        pass