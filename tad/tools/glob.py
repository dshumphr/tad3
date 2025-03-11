import glob
import os

class GlobTool:
    def schema(self):
        return {
            "name": "glob",
            "description": "Find files matching a pattern",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern (e.g., *.py)"}
                },
                "required": ["pattern"]
            }
        }

    def execute(self, args):
        pattern = os.path.abspath(args["pattern"])
        return "\n".join(glob.glob(pattern, recursive=True))

    @staticmethod
    def prompt():
        return "Find files matching [pattern]. Return paths."