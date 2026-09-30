import wave

import av
import torch


TARGET_SAMPLE_RATE = 16000


class AudioProcessor:

    def load_audio(
        self,
        audio_path: str,
    ) -> torch.Tensor:

        container = av.open(audio_path)

        try:
            audio_stream = container.streams.audio[0]

            resampler = av.audio.resampler.AudioResampler(
                format="s16",
                layout="mono",
                rate=TARGET_SAMPLE_RATE,
            )

            audio_samples = []

            for frame in container.decode(audio_stream):
                resampled_frames = resampler.resample(frame)

                for resampled_frame in resampled_frames:
                    array = resampled_frame.to_ndarray()

                    audio_samples.append(
                        torch.from_numpy(array)
                    )

            if not audio_samples:
                raise ValueError(
                    "No audio samples found."
                )

            audio = torch.cat(
                audio_samples,
                dim=1,
            )

            audio = audio.squeeze(0)

            audio = audio.float() / 32768.0

            return audio

        finally:
            container.close()

    def save_wav(
        self,
        audio: torch.Tensor,
        output_path: str,
    ) -> None:

        if audio.numel() == 0:
            raise ValueError(
                "Cannot save empty audio."
            )

        audio = audio.detach().cpu()

        audio = torch.clamp(
            audio,
            -1.0,
            1.0,
        )

        audio_int16 = (
            audio * 32767
        ).to(torch.int16)

        with wave.open(
            output_path,
            "wb",
        ) as wav_file:

            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(
                TARGET_SAMPLE_RATE
            )

            wav_file.writeframes(
                audio_int16.numpy().tobytes()
            )


audio_processor = AudioProcessor()