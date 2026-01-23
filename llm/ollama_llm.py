import requests
from config import OLLAMA_URL, LLM_MODEL

def generate(prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["message"]["content"]
