import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm.safe_generate import safe_generate

from llm.safe_generate import safe_generate

OUTPUT_DIR = "migrations"


def build_prompt(py_code: str, file_path: str) -> str:
    return f"""
You are an expert software migration engineer.

Convert the following Python code into Go.

Strict requirements:
- The Go code must produce the exact same output for the same inputs
- Preserve all logic and edge cases
- Use idiomatic Go
- Replace Python exceptions with explicit error handling
- Use proper Go types
- Do NOT omit any logic
- The output must be a complete, compilable Go file
- Include package name, imports, and main() if required

Python file path:
{file_path}

Python code:
----------------
{py_code}
----------------

Output:
- Full Go source code only
"""


def convert_python_to_go(python_file: str, code_content: str = None) -> str:
    if code_content is None:
        if not os.path.exists(python_file):
            raise FileNotFoundError(f"Python file not found: {python_file}")

        with open(python_file, "r", encoding="utf-8") as f:
            code_content = f.read()

    prompt = build_prompt(code_content, python_file)
    go_code = safe_generate(prompt)

    return go_code


def save_go_file(python_file: str, go_code: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base = os.path.basename(python_file).replace(".py", ".go")
    out_path = os.path.join(OUTPUT_DIR, base)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(go_code)

    print(f"Go file generated: {out_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python migrate/py_to_go.py <python_file>")
        sys.exit(1)

    py_file = sys.argv[1]

    go_code = convert_python_to_go(py_file)
    save_go_file(py_file, go_code)
