import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

print("Testing Gemini...")

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello in one sentence.",
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nFAILED!")
    print(type(e).__name__)
    print(e)