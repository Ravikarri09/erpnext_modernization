import faiss
import json
import numpy as np
from llm.ollama_embed import embed

def search(query, module, k=5):
    index = faiss.read_index(f"vector_db/{module}.index")

    with open(f"data/{module}_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    qvec = np.array([embed(query)]).astype("float32")
    _, indices = index.search(qvec, k)

    results = []
    for i in indices[0]:
        results.append(chunks[i]["text"])

    return results
