import io
from abc import ABC, abstractmethod

import sounddevice
import soundfile
import speech_recognition

from ratatai import logger
from ratatai.typing import Speech


class VoiceIO(ABC):
    """Class that should encapsulate the entire speech input/output functionality."""

    @abstractmethod
    def listen_single(self) -> Speech:
        """Blocking method that waits for speech input, captures it and converts to text."""

    @abstractmethod
    def speak(self, speech: Speech) -> None:
        """Blocking method that plays the given speech."""


class VoiceIOImpl(VoiceIO):
    def __init__(self, pause_thold: float) -> None:
        self._recognizer = speech_recognition.Recognizer()
        self._recognizer.pause_threshold = pause_thold

        self._microphone = speech_recognition.Microphone()

        self._setup()

    def _setup(self) -> None:
        logger.info("Adjusting ambient noise level, please wait...")

        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        logger.info("Ready!")

    def listen_single(self) -> Speech:
        with self._microphone as source:
            audio = self._recognizer.listen(
                source, timeout=None, phrase_time_limit=None, stream=False
            )
        audio_bytes: bytes = audio.get_wav_data()

        return Speech(audio_bytes)

    def speak(self, speech: Speech) -> None:
        data, _ = soundfile.read(io.BytesIO(speech), dtype="float32")
        # Wait until playback is finished
        sounddevice.play(data)
        sounddevice.wait()
