from migrate.python_to_go import build_prompt, convert_python_to_go, save_go_file
import os


def test_build_prompt_contains_code_and_path():
    py_code = "print('hello')"
    file_path = "sample.py"

    prompt = build_prompt(py_code, file_path)

    assert "Convert the following Python code into Go" in prompt
    assert py_code in prompt
    assert file_path in prompt


def test_converter_returns_string(tmp_path):
    py_file = tmp_path / "test.py"
    py_file.write_text("print('hello')")

    go_code = convert_python_to_go(str(py_file))

    assert isinstance(go_code, str)
    assert len(go_code) > 0


def test_go_file_is_created(tmp_path):
    python_file = tmp_path / "x.py"
    python_file.write_text("print('hi')")

    go_code = "package main"

    os.chdir(tmp_path)
    save_go_file(str(python_file), go_code)

    assert os.path.exists("migrations/x.go")
