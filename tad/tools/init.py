import os
import glob
import re
import subprocess

class InitCodebaseTool:
    def schema(self):
        return {
            "name": "init",
            "description": "Initialize AI.md with codebase info",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

    def execute(self, args):
        cwd = os.getcwd()
        description = self._infer_description(cwd)
        commands = self._infer_commands(cwd)
        style = self._infer_style(cwd)
        content = self._generate_ai_md(description, commands, style)
        ai_md_path = os.path.join(cwd, "AI.md")
        with open(ai_md_path, "w") as f:
            f.write(content)
        return f"Created AI.md at {ai_md_path}"

    def _infer_description(self, cwd):
        # Try README.md first
        readme_path = os.path.join(cwd, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                lines = [line.strip() for line in f.readlines()[:5] if line.strip()]
                if lines:
                    # Grab first non-empty line or two
                    return " ".join(lines[:2]) if len(lines) > 1 else lines[0]
        
        # Fallback: Check git or dir structure
        try:
            result = subprocess.run(
                "git log -1 --pretty=format:%s", 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0 and result.stdout:
                return f"Project based on recent work: {result.stdout}"
        except Exception:
            pass
        
        # Last resort: Dir-based guess
        top_dirs = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d)) and not d.startswith(".")]
        if top_dirs:
            return f"A project with components: {', '.join(top_dirs[:3])}."
        return "No project description inferred."

    def _infer_commands(self, cwd):
        commands = {"build": "", "test": "", "lint": ""}
        if os.path.exists(os.path.join(cwd, "package.json")):
            commands["build"] = "npm run build"
            commands["test"] = "npm test"
            commands["lint"] = "npm run lint"
        elif os.path.exists(os.path.join(cwd, "pyproject.toml")) or os.path.exists(os.path.join(cwd, "setup.py")):
            commands["build"] = "python setup.py build"
            commands["test"] = "pytest"
            commands["lint"] = "flake8"
        if not any(commands.values()):
            commands["test"] = "Run tests manually (no test command detected)"
        return commands

    def _infer_style(self, cwd):
        py_files = glob.glob(os.path.join(cwd, "*.py"))
        if not py_files:
            return "No style detected (no Python files found)"
        with open(py_files[0], "r") as f:
            lines = f.readlines()[:10]
        indent = "4 spaces"
        for line in lines:
            if line.startswith(" "):
                spaces = len(line) - len(line.lstrip(" "))
                indent = f"{spaces} spaces" if spaces % 2 == 0 else "mixed"
                break
        return f"PEP 8, {indent} indents"

    def _generate_ai_md(self, description, commands, style):
        return f"""# TAD Context

## Project Description
{description}

## Commands
- Build: {commands["build"]}
- Test: {commands["test"]}
- Lint: {commands["lint"]}

## Style
- {style}
"""

    @staticmethod
    def prompt():
        return "Initialize AI.md with repo description, build, test, and style info."