from ratatai import config
from ratatai.assistant import CookingAssistant
from ratatai.input_processor import MockInputProcessor
from ratatai.translator import MockTextToSpeech, WhisperSpeechToText
from ratatai.voice_io import VoiceIOImpl


def create_cooking_assistant() -> CookingAssistant:
    return CookingAssistant(
        voice_io=VoiceIOImpl(pause_thold=0.8),
        input_processor=MockInputProcessor(),
        text2speech=MockTextToSpeech(mock_wav_path=config.Files.MOCK_RESPONSE_PATH),
        speech2text=WhisperSpeechToText(model_size=config.Whisper.MODEL_SIZE),
    )
