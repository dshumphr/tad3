import os
import re

class GrepTool:
    def schema(self):
        return {
            "name": "grep",
            "description": "Search files for a pattern",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Regex pattern"},
                    "path": {"type": "string", "description": "Directory or file to search"}
                },
                "required": ["pattern", "path"]
            }
        }

    def execute(self, args):
        path = os.path.abspath(args["path"])
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        pattern = re.compile(args["pattern"])
        results = []
        if os.path.isfile(path):
            with open(path, "r") as f:
                for i, line in enumerate(f, 1):
                    if pattern.search(line):
                        results.append(f"{path}:{i}:{line.strip()}")
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        for i, line in enumerate(f, 1):
                            if pattern.search(line):
                                results.append(f"{file_path}:{i}:{line.strip()}")
        return "\n".join(results) if results else "No matches found."

    @staticmethod
    def prompt():
        return "Search [pattern] in [path]. Return matching lines."