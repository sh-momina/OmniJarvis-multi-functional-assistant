import tkinter as tk
from tkinter import scrolledtext
import threading
import asyncio
import time
import os
from queue import Queue
from dotenv import dotenv_values

# === Your Backend Modules ===
from Backend.Model import queryCategorization
from Backend.RealTimeSearchEngine import RealTimeSearchEngine
from Backend.Automation import Automation
from Backend.Chatbot import Chatbot
from Backend.SpeechToText import speechRecognation
from Backend.TextToSpeech import textToSpeech
from Backend.ImageGeneration import generate_image
from Backend.face_recognition.testModel import recognize_face
from Backend.gestureControl.testing import control

# === Load .env Variables ===
env = dotenv_values(".env")
Username = env.get("Username", "User")
AssistantName = env.get("AssistantName", "Jarvis")

# === Shared command queue ===
command_queue = Queue()
async_loop = asyncio.new_event_loop()

# Keep track of last command to avoid duplicates
last_command_from_gui = None
last_command_from_voice = None

# === GUI Class ===
class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{AssistantName} - AI Assistant")
        self.root.geometry("700x500")

        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.StringVar()
        self.input_entry = tk.Entry(root, textvariable=self.user_input, font=("Arial", 14))
        self.input_entry.pack(pady=5, fill=tk.X, padx=10)
        self.input_entry.bind("<Return>", self.on_enter)

        frame = tk.Frame(root)
        frame.pack(pady=10)
        tk.Button(frame, text="Send", command=self.on_enter, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.update_output(f"Welcome {Username}, how may I assist you today?")
        textToSpeech(f"Welcome {Username}, how may I assist you today?")

    def update_output(self, text):
        self.output_box.insert(tk.END, f"{AssistantName}: {text}\n")
        self.output_box.yview(tk.END)

    def on_enter(self, event=None):
        global last_command_from_gui
        query = self.user_input.get().strip()
        if not query:
            return
        self.user_input.set("")
        self.output_box.insert(tk.END, f"{Username}: {query}\n")

        # Deduplicate: Only add if different from last GUI command
        if query != last_command_from_gui:
            print(f"[GUI] Adding command to queue: {query}")
            command_queue.put(query)
            last_command_from_gui = query
        else:
            print(f"[GUI] Duplicate command ignored: {query}")

# === Async Task Processor ===
async def process_input_async(user_input, display_callback):
    try:
        categorized = queryCategorization(user_input)
        print("📌 Categorized as:", categorized)

        for command in categorized:
            
            if "presentation" in command.lower():
                os.startfile(r"D:\study\semester 6\Artifitial intellegence\content\1.1  Ai Agents.pptx")
                control()
                
            elif command.startswith("general "):
                response = Chatbot(command.replace("general ", ""))
                display_callback(response)
                textToSpeech(response)

            elif command.startswith("realtime "):
                response = RealTimeSearchEngine(command.replace("realtime ", ""))
                display_callback(response)
                textToSpeech(response)

            elif command.startswith("generate image "):
                generate_image(command)
                display_callback(f"🖼️ Image generated for: {command}")

            elif command.startswith(("open_and_type ", "close ", "play ", "content ", "google search", "youtube search", "system", "open ")):
                await Automation([command])
                print(f"[Automation] Executed command: {command}")
                response = f"✅ Executed: {command}"
                display_callback(response)
                # textToSpeech(response)

            elif command == "exit":
                goodbye = "Goodbye!"
                display_callback(goodbye)
                textToSpeech(goodbye)
                break

            else:
                response = f"Unhandled command: {command}"
                display_callback(response)
                textToSpeech(response)

    except Exception as e:
        print("❌ Error in process_input_async:", e)
        error_text = f"Error: {e}"
        display_callback(error_text)
        textToSpeech(error_text)

# === Background Task Consumer ===
async def command_consumer(display_callback):
    while True:
        if not command_queue.empty():
            query = command_queue.get()
            await process_input_async(query, display_callback)
        await asyncio.sleep(0.1)

# === Background Voice Listener Thread ===
def voice_listener():
    global last_command_from_voice
    print("🟡 Voice Listener started...")
    while True:
        try:
            query = speechRecognation()
            if query:
                print(f"🎤 Voice command received: {query}")
                if query.lower() in ["exit", "quit", "goodbye"]:
                    if query != last_command_from_voice:
                        command_queue.put(query)
                        last_command_from_voice = query
                    break

                # Deduplicate voice commands same as last
                if query != last_command_from_voice:
                    command_queue.put(query)
                    last_command_from_voice = query
                else:
                    print(f"[Voice] Duplicate command ignored: {query}")
        except Exception as e:
            print(f"🎙️ Voice error: {e}")
        time.sleep(0.5)

# === Main Launcher ===
if __name__ == "__main__":
    if recognize_face():
        textToSpeech("User validated")
        print(f"🚀 {AssistantName} is starting...")

        root = tk.Tk()
        app = AssistantApp(root)

        # Start asyncio event loop in background
        def run_async_loop():
            asyncio.set_event_loop(async_loop)
            async_loop.run_until_complete(command_consumer(app.update_output))

        threading.Thread(target=run_async_loop, daemon=True).start()

        # Start voice listener in background
        threading.Thread(target=voice_listener, daemon=True).start()

        root.mainloop()
    else:
        textToSpeech("Invalid User, Unable to login")
