# import torch
# from pathlib import Path

# from app.services.audio.processor import (
#     audio_processor,
# )
# from app.services.stt.manager import (
#     stt_manager,
# )
# from app.services.voice.vad import (
#     vad_service,
# )


# class VoiceInputService:

#     def process_audio(
#         self,
#         audio_path: str,
#     ) -> str:

#         audio_file = Path(audio_path)

#         if not audio_file.exists():
#             raise FileNotFoundError(
#                 f"Audio file not found: {audio_path}"
#             )

#         # 1. Load audio
#         audio = audio_processor.load_audio(
#             str(audio_file)
#         )

#         # 2. Detect and extract speech
#         speech_segments = (
#             vad_service.extract_speech(audio)
#         )

#         if not speech_segments:
#             return ""

#         # 3. Combine speech segments
#         speech_audio = torch.cat(
#             speech_segments
#         )

#         # 4. Save speech audio
#         output_path = (
#             "tests/voice_input.wav"
#         )

#         audio_processor.save_wav(
#             speech_audio,
#             output_path,
#         )

#         # 5. Convert speech to text
#         transcript = (
#             stt_manager.transcribe(
#                 output_path
#             )
#         )

#         return transcript


# voice_input_service = VoiceInputService()

from pathlib import Path

import torch

from app.services.audio.processor import (
    audio_processor,
)
from app.services.stt.manager import (
    stt_manager,
)
from app.services.voice.vad import (
    vad_service,
)


class VoiceInputService:

    def process_audio(
        self,
        audio_path: str,
        speech_output_path: str = "tests/voice_input.wav",
    ) -> str:

        audio_file = Path(audio_path)

        if not audio_file.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        # 1. Load audio
        audio = audio_processor.load_audio(
            str(audio_file)
        )

        # 2. Detect and extract speech
        speech_segments = (
            vad_service.extract_speech(audio)
        )

        if not speech_segments:
            return ""

        # 3. Combine speech segments
        speech_audio = torch.cat(
            speech_segments
        )

        # 4. Save extracted speech audio
        output_path = Path(
            speech_output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        audio_processor.save_wav(
            speech_audio,
            str(output_path),
        )

        # 5. Convert speech to text
        transcript = (
            stt_manager.transcribe(
                str(output_path)
            )
        )

        return transcript


voice_input_service = VoiceInputService()