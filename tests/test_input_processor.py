from ratatai.dot_env import get_api_key
from ratatai.input_processor import OpenAiInputProcessor

if __name__ == "__main__":
    recipe_steps = [
        "Add eggs and milk.",
        "Stir well.",
        "Pour into the dish and bake for 25 minutes.",
    ]
    input_processor = OpenAiInputProcessor(
        recipe_steps, openai_api_key=get_api_key("openai")
    )
    print(input_processor.generate_response("What should I do next?"))
