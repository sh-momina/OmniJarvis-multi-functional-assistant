from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_variables = dotenv_values(".env")

username = env_variables.get("Username")
AssistanName = env_variables.get("AssistanName")
GroqAPIKey = env_variables.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {username}, You are a very accurate and advanced AI chatbot named {AssistanName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatbot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\log.json", "r") as sample:
        messages = load(sample)
except FileNotFoundError:
    with open(r"Data\log.json", "w") as sample:
        dump([], sample)

def RealTimeInfo():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = "please use this real time information if needed" + "\n"
    data += "Day :"+ day + "\n" +"Date :"+ date + "\n" +"Month :"+ month + "\n" 
    data += "Year :"+ year + "\n" +"Hour :"+ hour + "\n" +"Minute :"+ minute + "\n" +"Second :"+ second + "\n"
    return data

def AnswerModifier(text):
    lines = text.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def Chatbot(query):
    try:
        with open(r"Data\log.json", "r") as sample:
            messages = load(sample)

        messages.append({"role":"user", "content":query})

        completion = client.chat.completions.create(
            model= "llama3-70b-8192",
            messages= SystemChatbot + [{"role":"system", "content":RealTimeInfo()}] + messages,
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

        messages.append({"role":"assistant", "content": answer})

        with open(r"Data\log.json", "w") as sample:
            dump(messages,sample,indent=4)

        return AnswerModifier(answer)
    
    except Exception as e:
        print("Error : ",e)
        with open(r"Data\log.json", "w") as sample:
            dump([],sample, indent=4)
        return Chatbot(query)
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question : ")
        print(Chatbot(user_input))

        

    

 