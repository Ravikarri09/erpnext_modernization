from rag.retriever import search
from llm.safe_generate import safe_generate


def answer(question):
    """
    Main RAG pipeline:
    - Retrieve relevant code chunks
    - Build context
    - Ask LLM
    - Append file references
    """

    results = search(question)

    context = ""
    references = []

    for r in results:
        context += r["text"] + "\n"
        references.append(r["file"])

    prompt = f"""
You are an expert on the ERPNext codebase.

## Context
{context}

## Question
{question}

## Instructions
- Base your answer only on the provided context
- Explain clearly
- If code is relevant, include it
"""

    response = safe_generate(prompt)

    # Attach file references
    if references:
        ref_text = "\n\n References:\n" + "\n".join(set(references))
        response += ref_text

    return response


def stream_answer(question):
    """
    Streaming wrapper around answer()
    Sends tokens word-by-word
    """

    response = answer(question)

    for word in response.split():
        yield word + " "
