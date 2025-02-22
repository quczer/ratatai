from abc import ABC, abstractmethod

from ratatai.typing import Speech


class VoiceIO(ABC):
    """Class that should encapsulate the entire speech input/output functionality."""

    @abstractmethod
    def listen(self) -> Speech:
        """Blocking method that waits for speech input, captures it and converts to text."""

    @abstractmethod
    def speak(self, speech: Speech) -> None:
        """Blocking method that plays the given speech."""
