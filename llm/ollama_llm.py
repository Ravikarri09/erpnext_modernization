import requests
from config import OLLAMA_URL, LLM_MODEL

def generate(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )

    data = response.json()

    # Debug-friendly + safe handling
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]

    if "response" in data:  # fallback (older formats)
        return data["response"]

    raise RuntimeError(f"Ollama returned unexpected response: {data}")
