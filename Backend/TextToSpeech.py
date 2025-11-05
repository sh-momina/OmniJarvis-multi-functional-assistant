import win32com.client
import asyncio
import os
import edge_tts

speaker = win32com.client.Dispatch("SAPI.SpVoice")

async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"
    os.makedirs("Data", exist_ok=True)

    if os.path.exists(file_path):
        os.remove(file_path)

    communicate = edge_tts.Communicate(text, pitch="+5Hz", rate="+15%")
    await communicate.save(file_path)

def textToSpeech(text):
    speaker.Speak(text)

if __name__ == "__main__":
    while True:
        text_to_speak = input("Enter text to speak: ")
        
        if text_to_speak.lower() == "exit":
            break
        textToSpeech(text_to_speak)
        asyncio.run(TextToAudioFile(text_to_speak))
