import argparse
import os
from prompt_toolkit import PromptSession
from .agent import Agent

def run(args=None):
    parser = argparse.ArgumentParser(description="TAD: Tool-Assisted Developer")
    if args is not None:  # For testing, skip parsing
        pass
    else:
        parser.parse_args()

    print("╭──────────────────────────────╮")
    print("│ ✻ Welcome to TAD v0.1.0!    │")
    print("╰──────────────────────────────╯")
    print(f"  cwd: {os.getcwd()}")
    print("  Type /help for commands, Ctrl-C to exit.")

    agent = Agent()
    session = PromptSession("> ")

    while True:
        try:
            cmd = session.prompt()
            if isinstance(cmd, KeyboardInterrupt):  # Handle mock exception
                raise cmd
            if cmd.startswith("/"):
                if cmd == "/help":
                    print("Commands:")
                    print("  /help    - Show this help")
                    print("  /init    - Create AI.md with repo info")
                    print("  /compact - Summarize and trim conversation")
                    print("Tools: read, write, edit, bash, list, glob, grep, init")
                elif cmd == "/init":
                    response = agent.process("Run the init tool to create AI.md")
                    print(response)
                elif cmd == "/compact":
                    agent.compact_history()
                    print("Conversation compacted.")
                else:
                    print(f"Unknown command: {cmd}")
            else:
                response = agent.process(cmd)
                if isinstance(response, str):
                    print(response)
                elif response.get("needs_confirmation"):
                    print(f"Proposed edit: {response['description']}")
                    confirm = session.prompt("Apply? (y/n): ").lower() == "y"
                    if confirm:
                        result = agent.execute_tool(response["tool_call"])
                        print(result)
                    else:
                        print("Edit discarded.")
        except KeyboardInterrupt:
            print("\nAdios, partner!")
            break

if __name__ == "__main__":
    run()