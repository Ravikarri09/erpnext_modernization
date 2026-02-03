import json
import sys
import os
import faiss
import numpy as np


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm.ollama_embed import embed


DATA_DIR = "data"
VECTOR_DIR = "vector_db"

def build_index(module):
    chunk_file = f"{DATA_DIR}/{module}_chunks.json"

    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    vectors = []
    for chunk in chunks:
        vectors.append(embed(chunk["text"]))

    vectors = np.array(vectors).astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    os.makedirs(VECTOR_DIR, exist_ok=True)
    faiss.write_index(index, f"{VECTOR_DIR}/{module}.index")

    print(f"✅ Vector index built for module: {module}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python module_vector_store.py <module>")
        sys.exit(1)

    build_index(sys.argv[1])
