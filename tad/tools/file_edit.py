import os

class FileEditTool:
    def schema(self):
        return {
            "name": "edit",
            "description": "Edit a file by replacing text",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file"},
                    "old_string": {"type": "string", "description": "Text to replace"},
                    "new_string": {"type": "string", "description": "New text"}
                },
                "required": ["file_path", "old_string", "new_string"]
            }
        }

    def execute(self, args):
        file_path = os.path.abspath(args["file_path"])
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r") as f:
            content = f.read()
        if args["old_string"] not in content:
            raise ValueError(f"Text '{args['old_string']}' not found in {file_path}")
        new_content = content.replace(args["old_string"], args["new_string"], 1)
        with open(file_path, "w") as f:
            f.write(new_content)
        return f"Edited {file_path}"

    @staticmethod
    def prompt():
        return "Edit [file_path]: replace [old_string] with [new_string]."