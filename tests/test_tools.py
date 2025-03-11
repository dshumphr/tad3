import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tad.tools import get_tool_instances

@pytest.fixture
def tools():
    return get_tool_instances()

def test_read_tool(tools):
    ai_md_path = os.path.join(os.getcwd(), "AI.md")
    result = tools["read"].execute({"file_path": ai_md_path})
    assert "TAD Context" in result

def test_write_tool(tools, tmp_path):
    test_file = tmp_path / "test.txt"
    result = tools["write"].execute({"file_path": str(test_file), "content": "Hello"})
    assert "Wrote to" in result
    assert test_file.read_text() == "Hello"

def test_bash_tool(tools):
    result = tools["bash"].execute({"command": "echo TEST"})
    assert "TEST" in result