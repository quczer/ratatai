from ratatai.dot_env import get_api_key
from ratatai.translator import ElevenLabsSpeech
from ratatai.voice_io import VoiceIOImpl


def main():
    translator = ElevenLabsSpeech(api_key=get_api_key("elevenlabs"))
    voice_io = VoiceIOImpl(pause_thold=0.5)
    speech = translator("Hello, world!")
    voice_io.speak(speech)


if __name__ == "__main__":
    main()
