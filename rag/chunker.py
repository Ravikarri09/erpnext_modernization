import json

with open("data/functions.json", "r", encoding="utf-8") as f:
    functions = json.load(f)

chunks = []

for fn in functions:
    chunks.append({
        "id": len(chunks),
        "text": f"Function {fn['name']} in {fn['file']} at line {fn['line']}",
        "file": fn["file"]
    })

with open("data/code_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)

print("✅ Code chunks created:", len(chunks))
