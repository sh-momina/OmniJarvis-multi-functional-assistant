import speech_recognition as sr
from deep_translator import GoogleTranslator

def speechRecognation():
    r = sr.Recognizer()
    r.energy_threshold = 300   # adjust if too sensitive / not sensitive
    r.pause_threshold = 0.8    # seconds of silence before it stops recording

    # list available microphones if needed
    # print(sr.Microphone.list_microphone_names())

    with sr.Microphone(device_index=2) as source:
        print("Listening... Please speak something.")
        try:
            # timeout=5 means wait max 5s for speech to start
            # phrase_time_limit=5 means capture max 5s of speech
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("⏳ Timeout: No speech detected.")
            return None

    try:
        query = r.recognize_google(audio, language="en-US")
        print(f"User said: {query}")

        translated_input = GoogleTranslator(source='auto', target='en').translate(query)
        print(f"Translated: {translated_input}")
        return translated_input

    except sr.UnknownValueError:
        print("❌ Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"🌐 Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    speechRecognation()


# import speech_recognition as sr

# print("Available microphones:")
# for i, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"{i}: {name}")