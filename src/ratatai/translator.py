import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import requests
import torch
import whisper

from ratatai import logger
from ratatai.typing import Speech


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


class ElevenLabsSpeech(TextToSpeech):
    """Implementation of text-to-speech using ElevenLabs API"""

    def __init__(
        self, api_key: str | None = None, voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    ):
        """
        Initialize ElevenLabs text-to-speech

        Args:
            api_key: ElevenLabs API key. If None, will try to get from ELEVENLABS_API_KEY env var
            voice_id: ElevenLabs voice ID to use (default is "rachel" voice)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in ELEVENLABS_API_KEY environment variable"
            )
        self.voice_id = voice_id

    def __call__(self, text: str) -> Speech:
        """
        Convert text to speech using ElevenLabs API

        Args:
            text: Text to convert to speech

        Returns:
            Speech object containing the audio data

        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return Speech(response.content)


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
