
import os
import requests
from PIL import Image
from dotenv import dotenv_values

env_variable = dotenv_values(".env")
huggingFaceAPIKey = env_variable.get("HuggingFaceAPIKey")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": "Bearer " + huggingFaceAPIKey
}

def generate_image(prompt):
    folder = "Data"
    os.makedirs(folder, exist_ok=True)

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        filepath = os.path.join(folder, "generated_image.png")
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        image = Image.open(filepath)
        image.show() 

# generate_image("a cat eating ice cream and driving")





