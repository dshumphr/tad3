import subprocess

class BashTool:
    def schema(self):
        return {
            "name": "bash",
            "description": "Run a bash command",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"}
                },
                "required": ["command"]
            }
        }

    def execute(self, args):
        result = subprocess.run(args["command"], shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return result.stdout

    @staticmethod
    def prompt():
        return "Run [command] in shell. Return output."