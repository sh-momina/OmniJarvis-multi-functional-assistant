















# env_variables = dotenv_values(".env")
# GroqAPIKey = env_variables.get("GroqAPIKey")

# classes = [ 
#     "zCubwf"
#     "hgkEle",
#     "LTKOO",
#     "sY7ric"
#     "ZOLCW",
#     "IZ6rdc"
#     "vlzY6d"
#     "webanswers-webanswers_table_webanswers-table", "DoNo ikb4Bb gsrt", "sXLa0e",
#     "Lwkfke",
#     "05uR6d LTK00",
#     "gsrt vk_bk FzvwSb YwPhnf",
#     "polqee"
#     "tw-Data-text tw-text-small tw-ta",
#     "VQF4g",
#     "qv3Wpe",
#     "kno-rdesc" ,
#     "SPZz6b"
# ]

# userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# client = Groq(api_key= GroqAPIKey)

# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there is anything else I can help you with",
#     "I am at your service, for any other additional questions or support, don't hesitate to ask"

# ]

# messages = []

# SystemChatbot = [
#     {"role": "system", "content": "hello i am " + os.environ["username"] + "You are a content writer. You have to write content like lette"}
# ]

# def GoogleSearch(query):
#     search(query)
#     return True

# def content(Topic):
    
#     def OpenNotebook(file):
#         text_editor = "notepad.exe"
#         subprocess.Popen([text_editor, file])

#     def ContentWrite(prompt):
#         messages.append({"role" : "user", "content" : prompt})

#         completion = client.chat.completions.create(
#             model= "llama3-70b-8192",
#             messages= SystemChatbot + messages,
#             max_tokens= 2048,
#             temperature= 0.7,
#             top_p= 1,
#             stream=True,
#             stop= None
#         )

#         answer = ""

#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 answer += chunk.choices[0].delta.content

#         answer = answer.replace("<s/>", "")

#         messages.append({"role":"assistant", "content": answer})

#         return answer
    
#     Topic : str = Topic.replace("Content", "")
#     ContentByAI = ContentWrite(Topic)

#     with open(rf"Data\{Topic.lower().replace(' ',' ')}.txt", "w", encoding = "utf-8") as file :
#         file.write(ContentByAI)
#         file.close()

#     OpenNotebook(rf"Data\{Topic.lower().replace(' ',' ')}.txt")
#     return True



# def YoutubeSearch(query):
#     Url4Search = f"HTTP://www.youtube.com/results?search_query={query}"
#     webbrowser.open(Url4Search)
#     return True

# def PlayYoutube(query):
#     playonyt(query)
#     return True


# def openApp(app, session = requests.session()):
#     try:
#         appopen(app, match_closest=True, output=True, throw_error=True)
#         return True
#     except:
#         def extractLink(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, "html.parser")
#             links = soup.find_all("a", {"jsname": "UWckNb"})
#             return [link.get("href") for link in links]
        
#         def search_google(query):
#             url = f"HTTP://www.youtube.com/search?q={query}"
#             headers = {"User-Agent" :  userAgent}
#             response = session.get(url, headers=headers)

#             if response.status_code == 200:
#                 return response.text
#             else:
#                 print("Failed to retrive search results")
#             return None
        
#         html = search_google(app)

#         if html:
#             link = extractLink(html)[0]
#             webopen(link)

#         return True
    
# def Closeapp(app):
#     if "chrome" in app:
#         pass
#     else:
#         try:
#             close(app, match_closest=True, output=True, throw_error=True)
#             return True
#         except:
#             return False
        
# def system(command):
    
#     def mute():
#         keyboard.press_and_release("volume mute")

#     def unmute():
#         keyboard.press_and_release("volume mute")

#     def volumeUp():
#         keyboard.press_and_release("volume up")

#     def volumeDown():
#         keyboard.press_and_release("volume down")

#     if command == "mute":
#         mute()
#     elif command == "unmute":
#         unmute()
#     elif command == "volume up":
#         volumeUp()
#     elif command == "volume down":
#         volumeDown()
#     return True

# async def TranslateAndExecute(command : list[str]):
#     if command.startswith("open "):
#         if "open it" in command:
#             pass
#         if "open file" == command:
#             pass
#         else:
#             fun = asyncio.to_thread(openApp, command.removeprefix("open "))
#             function.append(fun)
#     elif command.startswith("general "):
#         pass
#     elif command.startswith("realtime "):
#         pass
#     elif command.startswith("close "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("close "))
#             function.append(fun)
#     elif command.startswith("play "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("play "))
#             function.append(fun)
#     elif command.startswith("content "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("content "))
#             function.append(fun)
#     elif command.startswith("google search "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("google search "))
#             function.append(fun)
#     elif command.startswith("youtube search "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("youtube search "))
#             function.append(fun)
#     elif command.startswith("system "):
#             fun = asyncio.to_thread(openApp, command.removeprefix("system "))
#             function.append(fun)
#     else:
#         print("no function found for " + command)

#     results = await asyncio.gather(*function)

#     for result in results:
#         if isinstance(result, str):
#             yield result
#         else:
#             yield result
            
# async def Automation(commands : list[str]):
#     async for result in TranslateAndExecute(commands):
#         pass
#     return True


# openApp("facebook")




