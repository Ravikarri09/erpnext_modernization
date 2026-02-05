from llm.openai_llm import generate as ollama_generate

def safe_generate(prompt: str) -> str:
    return ollama_generate(prompt)
