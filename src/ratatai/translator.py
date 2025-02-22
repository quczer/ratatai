from abc import ABC, abstractmethod

from ratatai.typing import Speech


class Translator(ABC):
    """Class responsible for doing text-to-speech and speech-to-text translations."""

    @abstractmethod
    def text_to_speech(self, text: str) -> Speech:
        pass

    @abstractmethod
    def speech_to_text(self, speech: Speech) -> str:
        pass
