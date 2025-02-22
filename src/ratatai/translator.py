from abc import ABC, abstractmethod

from ratatai.typing import Speech


class TextToSpeech(ABC):
    @abstractmethod
    def __call__(self, text: str) -> Speech:
        pass


class SpeechToText(ABC):
    @abstractmethod
    def __call__(self, speech: Speech) -> str:
        pass
