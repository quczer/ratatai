from ratatai.voice_io import VoiceIOImpl

if __name__ == "__main__":
    voice_io = VoiceIOImpl()

    while True:
        try:
            print("Listening...")
            speech = voice_io.listen_single()
            print(f"Got {len(speech)} bytes of audio data.")
            print("Repeating...")
            voice_io.speak(speech)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
