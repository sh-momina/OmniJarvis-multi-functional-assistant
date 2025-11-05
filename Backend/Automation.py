from AppOpener import close, open
from webbrowser import open 
from dotenv import dotenv_values
from AppOpener import open as appopen
from pywhatkit import playonyt
from pywhatkit import search
from rich import print
import webbrowser
import subprocess
from groq import Groq
import os
import asyncio
import keyboard
import pyautogui
import time

env = dotenv_values(".env")
GroqAPIKey = env.get("GroqAPIKey")

def generate_ai_content(prompt):
    
    client = Groq(api_key=GroqAPIKey)

    messages = [{"role": "system", "content": "You are a helpful content writer."},
                {"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        max_tokens=1000,
        stream=True
    )

    result = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            result += chunk.choices[0].delta.content
    return result.strip()

def write_and_open_file(content, title):
    os.makedirs("Data", exist_ok=True)
    filename = f"Data/{title.replace(' ', '_').lower()}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    subprocess.Popen(["notepad.exe", filename])
    
def generate_content_file(topic):
    print(generate_ai_content(topic))
    return 

    
def open_and_type(commands):
    print(" open_and_type called with:", commands)
    commands_lower = commands.lower()
    text = extract_text_after_type(commands)

    if "command prompt" in commands_lower:
        subprocess.Popen("start cmd", shell=True)
        time.sleep(1.5)
        pyautogui.write(text, interval=0.1)

    elif "notepad" in commands_lower:
        subprocess.Popen(["notepad.exe"])
        time.sleep(1.5)
        pyautogui.write(text, interval=0.1)

def extract_text_after_type(command):
    lowered = command.lower()
    if "type" in lowered:
        return command.split("type", 1)[-1].strip()
    elif "write" in lowered:
        return command.split("write", 1)[-1].strip()
    return ""


def open_app(app_name):
    try:
        appopen(app_name, match_closest=True, throw_error=True)
    except:
        print(app_name + " not found, searching this app")
        webbrowser.open("https://www.google.com/search?q=" + app_name)
        
def close_app(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def play_on_youtube(query):
    playonyt(query)

def search_youtube(query):
    webbrowser.open("https://www.youtube.com/results?search_query=" + query)

def search_google(query):
    search(query)
    
def system(command):
    
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volumeUp():
        keyboard.press_and_release("volume up")

    def volumeDown():
        keyboard.press_and_release("volume down")
        
    def pause():
        keyboard.press_and_release("pause")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volumeUp()
    elif command == "volume down":
        volumeDown()
    elif command == "pause":
        pause()
    return True
        
async def TranslateAndExecute(command : list[str]):
    
    function = []
    
    for command in command:
        
        if command.startswith("open_and_type "):
            fun = asyncio.to_thread(open_and_type, command.removeprefix("open_and_type "))
            function.append(fun)
        elif command.startswith("open "):
            fun = asyncio.to_thread(open_app, command.removeprefix("open "))
            function.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
                fun = asyncio.to_thread(close_app, command.removeprefix("close "))
                function.append(fun)
        elif command.startswith("play "):
                fun = asyncio.to_thread(play_on_youtube, command.removeprefix("play "))
                function.append(fun)
        elif command.startswith("content "):
                fun = asyncio.to_thread(generate_content_file, command.removeprefix("content "))
                function.append(fun)
        elif command.startswith("google search "):
                fun = asyncio.to_thread(search_google, command.removeprefix("google search "))
                function.append(fun)
        elif command.startswith("youtube search "):
                fun = asyncio.to_thread(search_youtube, command.removeprefix("youtube search "))
                function.append(fun)
        elif command.startswith("system "):
                fun = asyncio.to_thread(system, command.removeprefix("system "))
                function.append(fun)   
        else:
            print("no function found for " + command)

    results = await asyncio.gather(*function)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result
            
async def Automation(commands : list[str]):
    
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    # generate_content_file("few lines about a famous book of roald dhal")
    # open_app("facebook")
    # play_on_youtube("atif aslam mashup 2025")
    # search_youtube("Digital marketing tips")
    # open_and_type("open command prompt and type hello")
    # search_google("How does GPT-4 work?")
    # system("volume down")
    # close_app("setings")
    asyncio.run(Automation(["open facebook", "play atif aslam mashaup" ,"content write two line s about elon musk", "open sttings", "close settingds", "system mute"]))

        
            
            
            
            
            
            

