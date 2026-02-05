import os
import re
from pathlib import Path
from typing import Tuple

from llm.safe_generate import safe_generate


class GoMigrationEngine:
    """
    Python → Go migration engine for ERPNext code.

    Responsibilities:
    - Prompt construction
    - LLM invocation (via safe_generate)
    - Output sanitization
    - Static validation
    """

    # ============================
    # Prompt Construction
    # ============================

    def build_prompt(self, py_code: str, file_path: str) -> str:
        return f"""
You are a senior Go engineer migrating ERPNext Python code to Go.

STRICT RULES:
- Output ONLY valid Go code
- Start with: package main
- No markdown, no explanations
- The Go program MUST compile
- The Go output MUST match Python behavior
- Preserve all logic and edge cases
- Use idiomatic Go
- Use explicit error handling
- Never omit logic

Python file:
{file_path}

Python code:
----------------
{py_code}
----------------
"""

    # ============================
    # Public API
    # ============================

    def migrate_file(self, python_file: str) -> str:
        python_file = Path(python_file)

        if not python_file.exists():
            raise FileNotFoundError(f"File not found: {python_file}")

        py_code = python_file.read_text(encoding="utf-8")

        prompt = self.build_prompt(py_code, str(python_file))
        raw_go = safe_generate(prompt)

        go_code = self._clean_go_code(raw_go)
        self._validate_go(go_code)

        return go_code

    def save_go_file(self, python_file: str, go_code: str) -> Path:
    
        project_root = Path(__file__).resolve().parents[1]
        out_dir = project_root / "migrations"
        out_dir.mkdir(exist_ok=True)

        python_file = Path(python_file)
        go_path = out_dir / (python_file.stem + ".go")

        go_path.write_text(go_code, encoding="utf-8")

        print(f"Go file generated: {go_path}")
        return go_path


    def migrate_and_save(self, python_file: str) -> Path:
        go_code = self.migrate_file(python_file)
        return self.save_go_file(python_file, go_code)

    # ============================
    # Cleaning & Validation
    # ============================

    def _clean_go_code(self, raw: str) -> str:
        """
        Removes markdown, explanations, and fixes common LLM artifacts.
        """
        text = raw.strip()

        # Remove markdown blocks
        text = text.replace("```go", "").replace("```", "")

        lines = []
        for line in text.splitlines():
            stripped = line.strip()

            # Remove obvious non-code noise
            if stripped.lower().startswith("here is"):
                continue
            if stripped.lower().startswith("this code"):
                continue
            if stripped.startswith("#"):
                continue

            lines.append(line)

        text = "\n".join(lines).strip()

        # Ensure package main
        if not text.startswith("package"):
            text = "package main\n\n" + text

        return text

    def _validate_go(self, code: str):
        """
        Lightweight static checks to catch obvious LLM mistakes early.
        """
        if "package main" not in code:
            raise ValueError("Generated Go code missing `package main`")

        open_braces = code.count("{")
        close_braces = code.count("}")
        if open_braces != close_braces:
            raise ValueError(
                f"Brace mismatch: {{={open_braces}, }}={close_braces}"
            )

        # Very common LLM failure
        if "..." in code:
            raise ValueError("Variadic syntax (...) detected — invalid for migration")

        # Catch incomplete outputs
        if len(code.splitlines()) < 5:
            raise ValueError("Go code too short — likely truncated")

    # ============================
    # Optional: Future Extension
    # ============================

    def fix_with_error(self, broken_code: str, compiler_error: str) -> str:
        """
        (Optional future step)
        Given compiler errors, ask the LLM to fix the Go code.
        """
        prompt = f"""
Fix the following Go code using the compiler error.
Output ONLY corrected Go code.

Compiler error:
{compiler_error}

Go code:
----------------
{broken_code}
----------------
"""
        fixed = safe_generate(prompt)
        fixed = self._clean_go_code(fixed)
        self._validate_go(fixed)
        return fixed


# ============================
# CLI Support
# ============================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m migrate.go_migrator <python_file>")
        sys.exit(1)

    engine = GoMigrationEngine()
    engine.migrate_and_save(sys.argv[1])
