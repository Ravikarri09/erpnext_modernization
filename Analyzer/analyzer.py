import os
import ast
import json

ERP_CODE_FOLDER = "erpnext/erpnext"
OUTPUT_FOLDER = "output"

functions_data = []
classes_data = []
calls_data = []


def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except:
        return

    current_function = None

    for node in ast.walk(tree):

        # Extract functions
        if isinstance(node, ast.FunctionDef):
            functions_data.append({
                "name": node.name,
                "file": file_path,
                "line": node.lineno
            })
            current_function = node.name

        # Extract classes
        if isinstance(node, ast.ClassDef):
            classes_data.append({
                "name": node.name,
                "file": file_path,
                "line": node.lineno
            })

        # Detect function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called_function = node.func.id

                if current_function:
                    calls_data.append({
                        "caller": current_function,
                        "callee": called_function,
                        "file": file_path
                    })
print("\n🔍 Scanning folder:", ERP_CODE_FOLDER)

for root, dirs, files in os.walk(ERP_CODE_FOLDER):
    print("📂 Entering:", root)

    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            print("   📄 Reading:", filepath)
            analyze_file(filepath)


print("\n🔍 Analyzing ERPNext codebase...\n")

for root, dirs, files in os.walk(ERP_CODE_FOLDER):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            analyze_file(filepath)

# Save results
with open(os.path.join(OUTPUT_FOLDER, "functions.json"), "w") as f:
    json.dump(functions_data, f, indent=4)

with open(os.path.join(OUTPUT_FOLDER, "classes.json"), "w") as f:
    json.dump(classes_data, f, indent=4)

with open(os.path.join(OUTPUT_FOLDER, "calls.json"), "w") as f:
    json.dump(calls_data, f, indent=4)


print("===================================")
print("✅ Analysis Complete!")
print("Functions found:", len(functions_data))
print("Classes found:", len(classes_data))
print("Call relationships found:", len(calls_data))
print("📁 Output saved in /output folder")
print("===================================")
