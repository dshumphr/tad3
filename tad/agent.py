from anthropic import Anthropic
import os
from .tools import get_tool_schemas, get_tool_instances

class Agent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.history = []
        self.tool_schemas = get_tool_schemas()
        self.tool_instances = get_tool_instances()
        self.system_prompt = (
            "You’re TAD: Tool-Assisted Developer. Execute tools based on user input ONLY: "
            "- The current working directory (cwd) is {cwd}. "
            "- For ALL tools (e.g., 'edit', 'read', 'write'), assume non-absolute paths (e.g., 'test.txt') are relative to the cwd. "
            "- ALWAYS construct absolute paths by prepending the cwd to relative paths (e.g., {cwd} + '/test.txt'). "
            "- NEVER ask the user for absolute paths or clarification about paths—construct them automatically. "
            "- 'edit [file] [old] [new]': Use the ‘edit’ tool with the absolute path, old string, and new string. Propose the edit and apply it if confirmed (e.g., 'y'). "
            "- 'What's in [file]' or 'read [file]': Use ‘read’ with the absolute path, return contents. "
            "- 'write [file] with [content]': Use ‘write’ with the absolute path and content. "
            "- 'What’s here?' or directory queries: Use ‘list’. "
            "- If the input is unclear (e.g., missing parameters), return 'Clarify.' "
            "Execute tools immediately without describing actions or hesitating—return the tool’s output ONLY."
        ).format(cwd=os.getcwd())
        self.ai_md_path = os.path.join(os.getcwd(), "AI.md")
        self.load_ai_md()

    def load_ai_md(self):
        if os.path.exists(self.ai_md_path):
            with open(self.ai_md_path, "r") as f:
                self.ai_md_content = f.read()
        else:
            self.ai_md_content = "No AI.md found. Run /init to create one."

    def process(self, input_str):
        self.history.append({"role": "user", "content": input_str})
        context = self.history[-3:] if len(self.history) > 3 else self.history
        system_content = f"{self.system_prompt}\n\nAI.md Context:\n{self.ai_md_content}"
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            system=system_content,
            messages=context,
            max_tokens=1000,
            tools=self.tool_schemas
        )
        content = response.content
        print("Claude response content:", [str(block) for block in content])  # Debug
        results = []
        tool_result = None
        for block in content:
            if block.type == "tool_use":
                tool_name = block.name
                if tool_name in ["edit", "write"]:
                    tool_result = {
                        "needs_confirmation": True,
                        "tool_call": block,
                        "description": f"{tool_name} {block.input}"
                    }
                    results.append(tool_result)
                else:
                    result = self.execute_tool(block)
                    self.history.append({"role": "assistant", "content": result})
                    results.append(result)
                    tool_result = result
            elif block.type == "text":
                text = block.text
                self.history.append({"role": "assistant", "content": text})
                results.append(text)
        return tool_result if tool_result else (results[-1] if results else "No actionable response from Claude.")

    def execute_tool(self, tool_call):
        tool = self.tool_instances[tool_call.name]
        return tool.execute(tool_call.input)

    def compact_history(self):
        if len(self.history) <= 3:
            return
        old_history = self.history[:-3]
        summary_prompt = (
            "Summarize this conversation concisely, focusing on key actions and info:\n"
            + "\n".join(f"{msg['role']}: {msg['content']}" for msg in old_history)
        )
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            system="Summarize concisely.",
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=200
        )
        summary = response.content[0].text
        self.history = [{"role": "assistant", "content": f"Summary: {summary}"}] + self.history[-3:]