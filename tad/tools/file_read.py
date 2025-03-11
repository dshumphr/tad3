import os

class FileReadTool:
    def schema(self):
        return {
            "name": "read",
            "description": "Read a file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the file"
                    }
                },
                "required": ["file_path"]
            }
        }

    def execute(self, args):
        file_path = os.path.abspath(args["file_path"])
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def prompt():
        return "Read a file at [file_path]. Return contents."