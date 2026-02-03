import json
import sys
import os

OUTPUT_DIR = "output"
DATA_DIR = "data"

def build_chunks(module):
    input_file = f"{OUTPUT_DIR}/{module}_functions.json"

    if not os.path.exists(input_file):
        raise Exception(f"Analyzer output not found for module: {module}")

    with open(input_file, "r", encoding="utf-8") as f:
        functions = json.load(f)

    chunks = []

    for fn in functions:
        chunks.append({
            "text": f"Function {fn['name']} in {fn['file']} at line {fn['line']}",
            "file": fn["file"],
            "module": module
        })

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(f"{DATA_DIR}/{module}_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Created {len(chunks)} chunks for module: {module}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python module_chunker.py <module>")
        sys.exit(1)

    build_chunks(sys.argv[1])
