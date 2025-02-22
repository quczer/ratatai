from abc import ABC, abstractmethod


class InputProcessor(ABC):
    """Class responsible for processing prompts from the user and generating responses based on loaded recipe.

    It should hold the state of the conversation and be able to generate responses based on the current state.
    """

    @abstractmethod
    def generate_response(self, text_prompt: str) -> str:
        pass


class MockInputProcessor(InputProcessor):
    def generate_response(self, text_prompt: str) -> str:
        return f"Mock response to {text_prompt}"
