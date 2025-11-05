from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_variables = dotenv_values(".env")
username = env_variables.get("Username")
AssistanName = env_variables.get("AssistanName")
GroqAPIKey = env_variables.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = (
    f"You are {AssistanName}, a professional AI assistant with real-time access via web search. "
    "Answer queries professionally using proper grammar, punctuation, and clarity."
)

messages = []
try:
    with open(r"Data\log.json", "r") as sample:
        messages = load(sample)
except FileNotFoundError:
    with open(r"Data\log.json", "w") as sample:
        dump([], sample)

def googleSearch(query):
    results = list(search(query, advanced=True, num_results=3))
    answer = ""
    for i in results:
        answer += f"Title: {i.title}\nDesc: {i.description}\n\n"
    return answer.strip()

def Info():
    now = datetime.datetime.now()
    return (
        "Real-time Info:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d %B %Y')}\n"
        f"Time: {now.strftime('%H:%M:%S')}"
    )

SystemChatbot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def RealTimeSearchEngine(query):
    global SystemChatbot, messages

    with open(r"Data\log.json", "r") as sample:
        messages = load(sample)
    messages = messages[-4:]
    messages.append({"role": "user", "content": query})

    search_content = googleSearch(query)
    info_content = Info()
    SystemChatbot.append({
        "role": "system",
        "content": search_content + "\n\n" + info_content
    })

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatbot + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )
    
    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.replace("<s/>", "")
    messages.append({"role": "assistant", "content": answer})

    with open(r"Data\log.json", "w") as sample:
        dump(messages, sample, indent=4)

    SystemChatbot.pop()
    return answer

if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")
        print(RealTimeSearchEngine(user_input))
