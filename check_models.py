import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("GOOGLE_API_KEY is missing from .env")
    exit()

client = genai.Client(api_key=api_key)

print("\nModels available for generateContent:\n")

for model in client.models.list():
    if model.supported_actions and "generateContent" in model.supported_actions:
        print(model.name)