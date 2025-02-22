from abc import ABC, abstractmethod


class CookingAssistant(ABC):
    """Class that should encapsulate the entire cooking assistant functionality.

    Interaction loop w/ the cooking assistant:
    > user presses [ENTER]
    > user says something
    > user presses [ENTER]
    > assistant generates a response
    """

    @abstractmethod
    def run(self) -> None:
        pass
