from abc import ABC, abstractmethod


class LLMService(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
    ):
        pass