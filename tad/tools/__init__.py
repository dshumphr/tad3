from .file_read import FileReadTool
from .file_write import FileWriteTool
from .file_edit import FileEditTool
from .bash import BashTool
from .list_files import ListFilesTool
from .glob import GlobTool
from .grep import GrepTool
from .init import InitCodebaseTool

def get_tool_schemas():
    tools = [
        FileReadTool(),
        FileWriteTool(),
        FileEditTool(),
        BashTool(),
        ListFilesTool(),
        GlobTool(),
        GrepTool(),
        InitCodebaseTool()
    ]
    return [t.schema() for t in tools]

def get_tool_instances():
    return {
        "read": FileReadTool(),
        "write": FileWriteTool(),
        "edit": FileEditTool(),
        "bash": BashTool(),
        "list": ListFilesTool(),
        "glob": GlobTool(),
        "grep": GrepTool(),
        "init": InitCodebaseTool()
    }