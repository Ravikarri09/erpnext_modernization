from llm.openai_llm import generate as openai_generate
from llm.ollama_llm import generate as ollama_generate

def safe_generate(prompt: str) -> str:
    try:
        return openai_generate(prompt)
    except Exception as e:
        print(" OpenAI failed, falling back to Ollama:", e)
        return ollama_generate(prompt)
