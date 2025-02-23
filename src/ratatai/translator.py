import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import requests
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


class ElevenLabsTTS(TextToSpeech):
    """Implementation of text-to-speech using ElevenLabs API"""

    _TTS_URL_FMT = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    
    def __init__(
        self, 
        api_key: str, 
        voice_id: str = "Ze8EnVlLm8458alzEofB",
        cache_size: int = 100
    ):
        self._api_key = api_key
        self._voice_id = voice_id
        self._cache = {}
        self._cache_size = cache_size

    def __call__(self, text: str) -> Speech:
        """
        Raises
        ------
            requests.exceptions.RequestException: If API call fails
        """
        # Check cache first
        if text in self._cache:
            return self._cache[text]

        url = ElevenLabsTTS._TTS_URL_FMT.format(voice_id=self._voice_id)
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self._api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "optimize_streaming_latency": 4  # Add streaming optimization
            },
        }

        # Use stream=True for streaming response
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        # Stream and concatenate chunks
        chunks = bytearray()
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunks.extend(chunk)

        speech = Speech(bytes(chunks))
        
        # Cache the result
        if len(self._cache) >= self._cache_size:
            # Remove oldest item if cache is full
            self._cache.pop(next(iter(self._cache)))
        self._cache[text] = speech

        return speech


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
