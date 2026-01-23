from llm.groq_llm import generate as generate_groq
from llm.ollama_llm import generate as generate_local

def safe_generate(prompt):
    try:
        return generate_groq(prompt)
    except:
        print("⚠️ Falling back to local Ollama")
        return generate_local(prompt)
