import json
import faiss
import numpy as np
from llm.ollama_embed import embed

MAX_CHUNKS = 100   # only process first 100 chunks

print("📦 Loading code chunks...")

with open("data/code_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Limit chunks for fast testing
chunks = chunks[:MAX_CHUNKS]

print("🔄 Generating embeddings for", len(chunks), "chunks (FAST MODE)...")

vectors = []

for i, chunk in enumerate(chunks):
    try:
        print(f"⚙️ Embedding chunk {i+1}/{len(chunks)}")
        vec = embed(chunk["text"])
        vectors.append(vec)
    except Exception as e:
        print("❌ Embedding failed:", e)

vectors = np.array(vectors).astype("float32")

print("📐 Vector shape:", vectors.shape)

if len(vectors) == 0:
    raise Exception("No embeddings generated. Check Ollama.")

dim = vectors.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(vectors)

faiss.write_index(index, "vector_db/faiss.index")

print("✅ Vector DB created with", len(vectors), "vectors (FAST MODE)")
