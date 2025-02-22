from ratatai import logger
from ratatai.input_processor import InputProcessor
from ratatai.translator import SpeechToText, TextToSpeech
from ratatai.voice_io import VoiceIO


class CookingAssistant:
    """Class that encapsulates the entire cooking assistant functionality."""

    def __init__(
        self,
        voice_io: VoiceIO,
        text2speech: TextToSpeech,
        speech2text: SpeechToText,
        input_processor: InputProcessor,
    ) -> None:
        self._voice_io = voice_io
        self._text2speech = text2speech
        self._speech2text = speech2text
        self._input_processor = input_processor

    def run(self) -> None:
        while True:
            self._repl_round()

    def _repl_round(self) -> None:
        logger.info("Listening...")
        user_speech = self._voice_io.listen()
        logger.debug(f"Got user speech of {len(user_speech)} bytes.")
        user_text = self._speech2text(user_speech)
        logger.info(f"Got user text: {user_text}")
        response_text = self._input_processor.generate_response(user_text)
        logger.info(f"Generated response: {response_text}")
        response_speech = self._text2speech(response_text)
        logger.debug(
            f"Generated response speech of {len(response_speech)} bytes. Speaking..."
        )
        self._voice_io.speak(response_speech)
        logger.debug("Spoke response.")
