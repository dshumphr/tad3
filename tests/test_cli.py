import pytest
from tad.cli import run

def test_cli_starts_and_exits(monkeypatch, capsys):
    monkeypatch.setattr("prompt_toolkit.PromptSession.prompt", lambda self: KeyboardInterrupt())
    run(args=[])  # Pass empty args to skip parsing
    captured = capsys.readouterr()
    assert "Welcome to TAD" in captured.out
    assert "Adios, partner!" in captured.out