# from google import genai

# from app.config.settings import settings
# from app.services.llm.base import LLMService


# MODEL_NAME = "gemini-3.5-flash-lite"


# class GeminiService(LLMService):

#     def __init__(self):
#         self.client = genai.Client(
#             api_key=settings.gemini_api_key
#         )

#     def generate(
#         self,
#         prompt: str,
#     ) -> str:

#         response = self.client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt,
#         )

#         return response.text

#     def stream(
#         self,
#         prompt: str,
#     ):
#         response = self.client.models.generate_content_stream(
#             model=MODEL_NAME,
#             contents=prompt,
#         )

#         for chunk in response:
#             if chunk.text:
#                 yield chunk.text


# gemini_service = GeminiService()

from collections.abc import AsyncIterator, Iterator

from google import genai

from app.config.settings import settings
from app.services.llm.base import LLMService


MODEL_NAME = "gemini-3.5-flash-lite"


class GeminiService(LLMService):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text

    def stream(self, prompt: str) -> Iterator[str]:
        response = self.client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=prompt,
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    async def stream_async(
        self,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        Stream Gemini response asynchronously.

        This will be used by the interruptible
        voice pipeline.
        """

        response = (
            await self.client.aio.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt,
            )
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text


gemini_service = GeminiService()