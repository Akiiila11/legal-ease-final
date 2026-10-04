import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-3.5-flash-lite"

if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not set. Add your Gemini API key to .env."
    )

client = genai.Client(api_key=API_KEY)


def generate_legal_text(prompt: str) -> str:
    max_attempts = 3

    print("\n========== GEMINI REQUEST ==========")
    print(f"Model: {MODEL_NAME}")
    print(f"Prompt length: {len(prompt)} characters")
    print(f"Prompt preview:\n{prompt[:1000]}")
    print("====================================\n")

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            text = (response.text or "").strip()

            if not text:
                raise ValueError("Empty response from Gemini")

            return text

        except Exception as exc:
            error_message = str(exc)

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if is_temporary_error and attempt < max_attempts - 1:
                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise RuntimeError(
                f"AI generation failed: {error_message}"
            ) from exc