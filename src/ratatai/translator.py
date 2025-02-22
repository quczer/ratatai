import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import torch
import whisper

from ratatai import logger
from ratatai.types import Speech


class TextToSpeech(ABC):
    @abstractmethod
    def __call__(self, text: str) -> Speech:
        pass


class SpeechToText(ABC):
    @abstractmethod
    def __call__(self, speech: Speech) -> str:
        pass


class MockTextToSpeech(TextToSpeech):
    def __init__(self, mock_wav_path: Path) -> None:
        self._speech = Speech(mock_wav_path.read_bytes())

    def __call__(self, text: str) -> Speech:  # noqa: ARG002
        return self._speech


class WhisperSpeechToText(SpeechToText):
    _LANGUAGE = "en"

    def __init__(self, model_size: str) -> None:
        self._whisper = whisper.load_model(model_size, device=torch.device("cuda"))

    def __call__(self, speech: Speech) -> str:
        logger.debug(f"{self.__class__.__name__} - Transcribing audio...")

        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp_file:
            tmp_file.write(speech)
            tmp_file.flush()

            # TODO: many config params here
            result = self._whisper.transcribe(
                tmp_file.name, language=WhisperSpeechToText._LANGUAGE
            )

        logger.debug("Done.")
        return result["text"]
