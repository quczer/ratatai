from abc import ABC, abstractmethod

from langchain.agents import AgentType, initialize_agent

# Import required LangChain components.
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import Tool


class InputProcessor(ABC):
    """Class responsible for processing prompts from the user and generating responses
    based on loaded recipe.

    It should hold the state of the conversation and be able to generate responses based on the current state.
    """

    @abstractmethod
    def generate_response(self, text_prompt: str) -> str:
        pass


class MockInputProcessor(InputProcessor):
    def generate_response(self, text_prompt: str) -> str:
        return f"Mock response to {text_prompt}"


class OpenAiInputProcessor(InputProcessor):
    def __init__(self, recipe_steps: list[str], openai_api_key: str):
        """
        Initializes the RecipeInputProcessor with the given recipe steps. It creates a LangChain agent
        configured with tools to mark individual steps as complete or finish the recipe.
        """
        self.recipe_steps = recipe_steps
        self.openai_api_key = openai_api_key

        # Track the current step (0-indexed) and the set of completed steps (steps are considered as 1-indexed).
        self.current_step = 0
        self.completed_steps = set[int]()
        self.finished = False

        # Create conversation memory.
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # Define tool functions that update the processor's state.
        def __mark_step_completed(step_number: int) -> str:
            self.completed_steps.add(step_number)
            return f"Step {step_number} marked as completed."

        def __finish_cooking(_: int) -> str:
            self.finished = True
            return "Congratulations! You've completed the recipe. Enjoy your meal!"

        # Define tools for the agent.
        mark_step_tool = Tool(
            name="MarkStepCompleted",
            func=__mark_step_completed,
            description="Marks a cooking step as completed. Input should be the step number.",
        )

        finish_cooking_tool = Tool(
            name="FinishCooking",
            func=__finish_cooking,
            description="Marks the entire cooking process as completed.",
        )

        # Build an initial system prompt that includes the recipe steps and the (empty) completed steps.
        system_prompt = f"""
        You are a helpful cooking assistant guiding users through a recipe step by step.

        Recipe Steps:
        {self.recipe_steps}

        Completed Steps:
        {sorted(self.completed_steps)}
        """
        self.memory.chat_memory.add_message(SystemMessage(content=system_prompt))

        # Initialize the LangChain language model.
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=self.openai_api_key,
        )

        # Initialize the agent with the two tools.
        self.agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=[mark_step_tool, finish_cooking_tool],
            llm=self.llm,
            verbose=False,
            memory=self.memory,
        )

    def generate_response(self, text_prompt: str) -> str:
        """
        Processes the incoming text prompt. Before handing off the user's message, the assistant injects a system
        message with the current recipe step instruction (if any). After the agent generates a response, the method:
         - checks if the current step got marked as completed (tools automatically update the processor state), and
         - if so, advances to the next step.
        """
        # If the recipe is finished, simply return a closing message.
        if self.finished:
            return "You've already completed the recipe. Enjoy your meal!"

        # If there is a current step, add a system message with its instruction.
        if self.current_step < len(self.recipe_steps):
            step_instruction = f"Please instruct the user to perform this step: {self.recipe_steps[self.current_step]}"
            self.memory.chat_memory.add_message(SystemMessage(content=step_instruction))
        else:
            # If no steps remain, mark finished automatically.
            self.finished = True
            self.memory.chat_memory.add_message(
                SystemMessage(content="All steps have been completed.")
            )
            return "Congratulations! You've completed the recipe. Enjoy your meal!"

        # Pass the user's prompt to the agent.
        response = self.agent.run(text_prompt)

        # Check if the agent (or user via the tool invocation) has marked the current step (which is 1-indexed)
        # as completed. For robustness, update the current step as long as the marking aligns.
        while (
            self.current_step + 1
        ) in self.completed_steps and self.current_step < len(self.recipe_steps):
            self.current_step += 1
            if self.current_step < len(self.recipe_steps):
                update_message = f"Moving on to the next step: {self.recipe_steps[self.current_step]}"
                self.memory.chat_memory.add_message(
                    SystemMessage(content=update_message)
                )

        return response
