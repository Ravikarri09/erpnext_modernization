import os
from pathlib import Path
import sys

# Ensure project root is on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from llm.safe_generate import safe_generate


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
def extract_go_code(llm_output: str) -> str:
    """
    Extract valid Go source code from LLM output.
    Ensures the file starts with `package`.
    """
    lines = llm_output.splitlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("package "):
            return "\n".join(lines[i:])

    raise ValueError("❌ No valid Go code found in LLM output")



<<<<<<< HEAD
def convert_python_to_go(python_file: str) -> str:
    python_file = Path(python_file)

    if not python_file.exists():
        raise FileNotFoundError(f"Python file not found: {python_file}")

    py_code = python_file.read_text(encoding="utf-8")
    prompt = build_prompt(py_code, str(python_file))

    raw_output = safe_generate(prompt)
    go_code = extract_go_code(raw_output)
    if "func main()" not in go_code:
        raise ValueError("Generated Go code missing main()")
=======
def convert_python_to_go(python_file: str, code_content: str = None) -> str:
    if code_content is None:
        if not os.path.exists(python_file):
            raise FileNotFoundError(f"Python file not found: {python_file}")

        with open(python_file, "r", encoding="utf-8") as f:
            code_content = f.read()

    prompt = build_prompt(code_content, python_file)
    go_code = safe_generate(prompt)
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d

    return go_code



def save_go_file(python_file: str, go_code: str) -> Path:
    """
    Save Go file next to the Python file inside a `migrations/` folder.
    This is REQUIRED for pytest functional tests.
    """
    python_file = Path(python_file)
    out_dir = python_file.parent / "migrations"
    out_dir.mkdir(exist_ok=True)

    go_file = out_dir / (python_file.stem + ".go")
    go_file.write_text(go_code, encoding="utf-8")

    print(f"Go file generated: {go_file}")
    return go_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate/python_to_go.py <python_file>")
        sys.exit(1)

    py_file = sys.argv[1]

    go_code = convert_python_to_go(py_file)
    save_go_file(py_file, go_code)
