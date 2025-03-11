import os

class FileWriteTool:
    def schema(self):
        return {
            "name": "write",
            "description": "Write a file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the file"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write"
                    }
                },
                "required": ["file_path", "content"]
            }
        }

    def execute(self, args):
        file_path = os.path.abspath(args["file_path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(args["content"])
        return f"Wrote to {file_path}"

    @staticmethod
    def prompt():
        return "Write [file_path] with [content]."