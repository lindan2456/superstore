import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_URL:
    raise RuntimeError("OLLAMA_URL not set. Check .env file.")
if not MODEL:
    raise RuntimeError("OLLAMA_MODEL not set. Check .env file.")


def call_llm(prompt: str) -> str:
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["response"]
