import os

class ListFilesTool:
    def schema(self):
        return {
            "name": "list",
            "description": "List files in a directory",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to directory"}
                },
                "required": ["path"]
            }
        }

    def execute(self, args):
        path = os.path.abspath(args["path"])
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Not a directory: {path}")
        return "\n".join(os.listdir(path))

    @staticmethod
    def prompt():
        return "List files in [path]. Return file names."