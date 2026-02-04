import subprocess
import sys
import os
from migrate.python_to_go import convert_python_to_go, save_go_file


def test_python_and_go_output_match(tmp_path):
    py_code = "print(2 + 3)"
    py_file = tmp_path / "test.py"
    py_file.write_text(py_code)

    # Run Python
    py_output = subprocess.check_output(
        [sys.executable, str(py_file)],
        text=True
    ).strip()

    # Convert to Go
    go_code = convert_python_to_go(str(py_file))
    go_file = save_go_file(str(py_file), go_code)

    # Step 1: Go syntax check
    syntax_check = subprocess.run(
        ["go", "fmt", str(go_file)],
        capture_output=True,
        env={**os.environ, "GO111MODULE": "off"}
    )

    assert syntax_check.returncode == 0, f"Invalid Go syntax:\n{syntax_check.stderr}"

    # Step 2: Execute Go
    go_output = subprocess.check_output(
        ["go", "run", str(go_file)],
        text=True,
        env={**os.environ, "GO111MODULE": "off"}
    ).strip()

    assert py_output == go_output


def test_generated_go_compiles(tmp_path):
    py_file = tmp_path / "a.py"
    py_file.write_text("print('hello')")

    go_code = convert_python_to_go(str(py_file))
    go_file = save_go_file(str(py_file), go_code)

    result = subprocess.run(
        ["go", "build", str(go_file)],
        capture_output=True,
        env={**os.environ, "GO111MODULE": "off"}
    )

    assert result.returncode == 0, result.stderr
