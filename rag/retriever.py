import json
import faiss
import numpy as np
from llm.ollama_embed import embed

# Load FAISS index
index = faiss.read_index("vector_db/faiss.index")

with open("data/code_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def search(query, k=5):
    query_vec = embed(query)
    query_vec = np.array([query_vec]).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append({
                "text": chunks[idx]["text"],
                "file": chunks[idx]["file"]
            })

    return results
