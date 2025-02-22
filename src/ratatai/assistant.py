from abc import ABC, abstractmethod


class CookingAssistant(ABC):
    """Class that should encapsulate the entire cooking assistant functionality."""

    @abstractmethod
    def run(self) -> None:
        pass
