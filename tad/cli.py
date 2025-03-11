import os
import sys
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from pygments.lexers.data import JsonLexer
from pygments.token import Token
from .agent import Agent

bindings = KeyBindings()

@bindings.add('c-c')
def _(event):
    event.app.exit(result='exit')

style = Style.from_dict({
    'success': '#00ff00',  # Green
    'error': '#ff0000',    # Red
    'prompt': '#ffff00',   # Yellow
    'info': '#0000ff',     # Blue
    'default': '#ffffff',  # White
    'path': '#00ffff',     # Cyan for file paths
    'json-key': '#0000ff',  # Blue for JSON keys
    'json-string': '#00ff00',  # Green for JSON strings
    'json-punctuation': '#ffffff',  # White for braces, colons
})

def run():
    agent = Agent()
    completer = WordCompleter(['/help', '/init', '/compact', 'edit', 'write', 'read', 'list'], ignore_case=True)
    session = PromptSession(
        "> ",
        completer=completer,
        key_bindings=bindings,
        style=style,
        multiline=False,
        complete_while_typing=True
    )

    welcome = HTML(
        "\n\n\n\n\n\n\n"
        "   <info>╭──────────────────────────────╮</info>\n"
        "   <info>│ ✻ Welcome to TAD v0.1.0!    │</info>\n"
        "   <info>╰──────────────────────────────╯</info>\n"
        f"   <info>cwd: {os.getcwd()}</info>\n"
        "   <info>Type /help for commands, Ctrl-C to exit.</info>"
    )
    print_formatted_text(welcome, style=style)

    while True:
        try:
            cmd = session.prompt()
            if not cmd:
                continue
            print(f"Processing command: {cmd}")
            if cmd == 'exit':
                break
            if cmd == '/help':
                print_formatted_text(HTML(
                    "<info>Commands:</info>\n"
                    "<default>  /help    - Show this help</default>\n"
                    "<default>  /init    - Create AI.md</default>\n"
                    "<default>  /compact - Compact conversation history</default>\n"
                    "<default>  edit     - Edit a file</default>\n"
                    "<default>  write    - Write to a file</default>\n"
                    "<default>  read     - Read a file</default>\n"
                    "<default>  list     - List directory contents</default>"
                ), style=style)
                continue
            response = agent.process(cmd)
            if isinstance(response, dict) and response.get("needs_confirmation"):
                tool_call = response["tool_call"]
                description = response["description"]
                edit_json = str(tool_call.input)
                # Tokenize with Pygments, build FormattedText manually
                lexer = JsonLexer()
                tokens = list(lexer.get_tokens(edit_json))
                formatted_tokens = []
                for ttype, value in tokens:
                    if ttype in Token.Literal.String:
                        formatted_tokens.append(('class:json-string', value))
                    elif ttype in Token.Name.Tag:
                        formatted_tokens.append(('class:json-key', value))
                    elif ttype in Token.Punctuation:
                        formatted_tokens.append(('class:json-punctuation', value))
                    else:
                        formatted_tokens.append(('class:default', value))
                formatted_json = FormattedText(formatted_tokens)
                print_formatted_text(HTML(
                    f"<prompt>Apply? (y/n):</prompt>"
                ), style=style)
                print_formatted_text(formatted_json, style=style)
                confirm = input("Apply? (y/n): ")
                if confirm.lower() == 'y':
                    result = agent.execute_tool(tool_call)
                    agent.history.append({
                        "role": "assistant",
                        "content": f"{description.split()[0]} completed"
                    })
                    if "write" in description:
                        print_formatted_text(HTML(f"<success>Wrote to <path>{tool_call.input['file_path']}</path></success>"), style=style)
                    elif "edit" in description:
                        print_formatted_text(HTML(f"<success>Edited</success>"), style=style)
                else:
                    agent.history.append({
                        "role": "assistant",
                        "content": f"{description.split()[0]} discarded"
                    })
                    print_formatted_text(HTML("<error>Edit discarded</error>"), style=style)
            elif cmd == '/compact':
                agent.compact_history()
                print_formatted_text(HTML("<success>Conversation compacted</success>"), style=style)
            elif response:
                print_formatted_text(HTML(f"<default>{response}</default>"), style=style)
                agent.history.append({"role": "assistant", "content": response})
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_msg = str(e).replace('<', '<').replace('>', '>')
            print_formatted_text(HTML(f"<error>{error_msg}</error>"), style=style)

    print_formatted_text(HTML("\n<info>Adios, partner!</info>"), style=style)

if __name__ == "__main__":
    run()