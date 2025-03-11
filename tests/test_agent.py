import pytest
from tad.agent import Agent
import os

class MockTextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text

class MockToolUseBlock:
    def __init__(self, name, input_data):
        self.type = "tool_use"
        self.name = name
        self.input = input_data

@pytest.fixture
def agent():
    return Agent()

def test_agent_text_response(agent, monkeypatch):
    class MockResponse:
        content = [MockTextBlock("Howdy!")]
    monkeypatch.setattr(agent.client, "messages", type("Mock", (), {"create": lambda *args, **kwargs: MockResponse})())
    assert agent.process("Say howdy") == "Howdy!"

def test_agent_tool_response(agent, monkeypatch):
    class MockResponse:
        content = [MockToolUseBlock("read", {"file_path": os.path.join(os.getcwd(), "AI.md")})]
    monkeypatch.setattr(agent.client, "messages", type("Mock", (), {"create": lambda *args, **kwargs: MockResponse})())
    result = agent.process("Read AI.md")
    assert "TAD Context" in result