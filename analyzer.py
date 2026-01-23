import os
import ast

# Path to ERPNext source code
ERP_CODE_FOLDER = "erpnext/erpnext"


def extract_functions(file_path):
    """Extract function names from a Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        tree = ast.parse(code)
    except Exception as e:
        return []

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return functions


print("\n🔍 Scanning ERPNext and extracting functions...\n")

total_functions = 0

for root, dirs, files in os.walk(ERP_CODE_FOLDER):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)

            functions = extract_functions(filepath)

            if functions:
                print(f"\n📄 File: {filepath}")
                for func in functions:
                    print("   -", func)
                total_functions += len(functions)

print("\n=================================")
print("✅ Total functions found:", total_functions)
print("=================================\n")
