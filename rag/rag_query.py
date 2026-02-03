from rag.retriever import search
from llm.safe_generate import safe_generate

def answer(question, module):
    context = "\n".join(search(question, module))

    prompt = f"""
You are an expert on the ERPNext {module} module.

## Context
{context}

## Question
{question}
"""

    return safe_generate(prompt)
