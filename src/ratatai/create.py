from ratatai import config
from ratatai.assistant import CookingAssistant
from ratatai.dot_env import get_api_key
from ratatai.input_processor import OpenAiInputProcessor
from ratatai.translator import ElevenLabsTTS, WhisperSpeechToText
from ratatai.voice_io import VoiceIOImpl


def create_cooking_assistant(recipe_steps: list[str]) -> CookingAssistant:
    return CookingAssistant(
        voice_io=VoiceIOImpl(pause_thold=1),
        input_processor=OpenAiInputProcessor(
            recipe_steps=recipe_steps, openai_api_key=get_api_key(key="openai")
        ),
        text2speech=ElevenLabsTTS(api_key=get_api_key(key="elevenlabs")),
        speech2text=WhisperSpeechToText(model_size=config.Whisper.MODEL_SIZE),
    )
