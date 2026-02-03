import os
import ast
import json
import sys

BASE_ERP_PATH = "erpnext/erpnext"
OUTPUT_FOLDER = "output"

functions_data = []
classes_data = []
calls_data = []


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        tree = ast.parse(code)
    except Exception:
        return

    current_function = None

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            functions_data.append({
                "name": node.name,
                "file": file_path,
                "line": node.lineno
            })
            current_function = node.name

        elif isinstance(node, ast.ClassDef):
            classes_data.append({
                "name": node.name,
                "file": file_path,
                "line": node.lineno
            })

        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if current_function:
                calls_data.append({
                    "caller": current_function,
                    "callee": node.func.id,
                    "file": file_path
                })


def analyze_module(module_name):
    module_path = os.path.join(BASE_ERP_PATH, module_name)

    if not os.path.exists(module_path):
        print(f"Module not found: {module_name}")
        sys.exit(1)

    print(f"\n🔍 Analyzing ERPNext module: {module_name}\n")

    for root, _, files in os.walk(module_path):
        for file in files:
            if file.endswith(".py"):
                analyze_file(os.path.join(root, file))


def save_output(module_name):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    with open(f"{OUTPUT_FOLDER}/{module_name}_functions.json", "w") as f:
        json.dump(functions_data, f, indent=2)

    with open(f"{OUTPUT_FOLDER}/{module_name}_classes.json", "w") as f:
        json.dump(classes_data, f, indent=2)

    with open(f"{OUTPUT_FOLDER}/{module_name}_calls.json", "w") as f:
        json.dump(calls_data, f, indent=2)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(" Please provide a module name")
        print(" Example: python analyzer.py accounts")
        sys.exit(1)

    module = sys.argv[1]

    analyze_module(module)
    save_output(module)

    print("\n===================================")
    print(" Analysis Complete!")
    print(" Module:", module)
    print(" Functions found:", len(functions_data))
    print(" Classes found:", len(classes_data))
    print(" Call relationships:", len(calls_data))
    print(" Output saved in /output folder")
    print("===================================")
