import pytest
import os
import subprocess
from pathlib import Path

@pytest.fixture
def temp_project(tmp_path):
    ai_md = tmp_path / "AI.md"
    ai_md.write_text(
        "# TAD Context\n"
        "## Project Description\nA test project.\n"
        "## Commands\n- Build: echo BUILD\n- Test: echo TEST\n"
        "## Style\n- Simple text"
    )
    test_file = tmp_path / "test.txt"
    test_file.write_text("Original content")
    yield tmp_path

def run_tad_command(commands, cwd=None):
    tad_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tad.py"))
    if isinstance(commands, str):
        commands = [commands]
    stdin = "\n".join(commands + ["\x03"])
    proc = subprocess.Popen(
        ["/opt/homebrew/bin/python3.11", tad_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd
    )
    stdout, stderr = proc.communicate(input=stdin, timeout=20)
    proc.wait()
    return stdout + stderr

def test_read_ai_md(temp_project):
    output = run_tad_command("What's in AI.md?", cwd=str(temp_project))
    print("test_read_ai_md output:\n", output)
    with open("test_read_ai_md.log", "w") as f:
        f.write(output)
    assert "A test project" in output, "Should read AI.md contents"
    assert "Simple text" in output

def test_write_confirmation_yes(temp_project):
    test_file = temp_project / "new.txt"
    output = run_tad_command(['write new.txt with "Hello"', "y"], cwd=str(temp_project))
    print("test_write_confirmation_yes output:\n", output)
    with open("test_write_yes.log", "w") as f:
        f.write(output)
    assert "Wrote to" in output, "Should confirm and write file"
    assert test_file.read_text() == "Hello", "File content should match"

def test_write_confirmation_no(temp_project):
    test_file = temp_project / "new.txt"
    output = run_tad_command(['write new.txt with "Hello"', "n"], cwd=str(temp_project))
    print("test_write_confirmation_no output:\n", output)
    with open("test_write_no.log", "w") as f:
        f.write(output)
    assert "Edit discarded" in output, "Should discard on 'n'"
    assert not test_file.exists(), "File should not be created"

def test_edit_confirmation(temp_project):
    test_file = temp_project / "test.txt"
    output = run_tad_command(['edit test.txt "Original" "New"', "y"], cwd=str(temp_project))
    print("test_edit_confirmation output:\n", output)
    with open("test_edit.log", "w") as f:
        f.write(output)
    assert "Edited" in output, "Should confirm and edit file"
    assert test_file.read_text() == "New content", "File should be edited"

def test_vague_prompt(temp_project):
    output = run_tad_command("What's here?", cwd=str(temp_project))
    print("test_vague_prompt output:\n", output)
    with open("test_vague.log", "w") as f:
        f.write(output)
    assert any(
        phrase in output.lower()
        for phrase in ["list", "dir", "files", "don’t understand", "Clarify"]
    ), "Should use 'list' tool or ask for clarity"

def test_compact_history(temp_project):
    commands = [
        "What's in AI.md?",
        'write log.txt with "Log entry"',
        "y",
        "list .",
        "/compact"
    ]
    output = run_tad_command(commands, cwd=str(temp_project))
    print("test_compact_history output:\n", output)
    with open("test_compact.log", "w") as f:
        f.write(output)
    assert "Conversation compacted" in output, "Should compact history"
    assert "Summary" in output or "compacted" in output, "Should mention summary"