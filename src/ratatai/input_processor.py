import openai
from abc import ABC, abstractmethod


class InputProcessor(ABC):
    """Class responsible for processing prompts from the user and generating responses
    based on loaded recipe.

    It should hold the state of the conversation and be able to generate responses based on the current state.
    """

    @abstractmethod
    def generate_response(self, text_prompt: str) -> str:
        pass


class OpenAiInputProcessor(InputProcessor):
    def __init__(self, recipe_steps: str, openai_api_key: str):
        """
        Initializes the RecipeAssistant with the recipe and a system prompt.
        """
        self.openai_api_key = openai_api_key
        self.recipe_steps = recipe_steps

        # Initialize the OpenAI client.
        self.client = openai.OpenAI(api_key=self.openai_api_key)

        # Initialize the conversation history with a system prompt.
        self.conversation_history = [
            {
                "role": "system",
                "content": f"""
                Yo, you’re the cooking bro here, guiding the user step-by-step through the recipe. Keep it chill—like you’re just hangin’ in the kitchen with a buddy. Break down each step one at a time, quick and easy. No rush, no stress—just straight-up good vibes and good food. Your job is to keep it casual, fast, and smooth. Let’s make this meal happen, one step at a time. Let’s do this!
                Here’s the recipe we’re tackling: 
                {self.recipe_steps}

                Start with text likie: I will help you today prepare some delicious scrambled eggs by Gordon ramsey.
                Your responses should be very quick so that the conversation keeps flowing nice (preferably one sentence).
                """,
            }
        ]

    def generate_response(self, text_prompt: str) -> str:
        """
        Generates a response from the assistant and updates the conversation history.
        """
        # Add the user's input to the conversation history.
        self.conversation_history.append({"role": "user", "content": text_prompt})

        # Get the assistant's response.
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use "gpt-3.5-turbo" for a faster/cheaper option
            messages=self.conversation_history,
            temperature=0.3,
        )

        # Extract the assistant's response.
        assistant_response = response.choices[0].message.content

        # Add the assistant's response to the conversation history.
        self.conversation_history.append({"role": "assistant", "content": assistant_response})

        return assistant_response