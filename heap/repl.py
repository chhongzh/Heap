"""
一个简单的repl实现
"""

FN_TYPES = ["int", "string", "float", "void"]
VA_TYPES = ["int", "string", "float"]

COMPLETE = {
    "var": {**dict([(name, None) for name in VA_TYPES])},
    "func": {**dict([(name, None) for name in FN_TYPES])},
    "continue": None,
    "return": None,
    ".help": None,
    ".exit": None,
}


def repl():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import NestedCompleter
    from prompt_toolkit.history import InMemoryHistory
    from .lexer import lex
    from .analyzer import Analyzer
    from .ast import ASTNode
    from .runner import Runner

    analyzer = Analyzer([])
    runner = Runner([])

    keyword_completer = NestedCompleter({})

    prompt = PromptSession(
        completer=keyword_completer, history=InMemoryHistory(), complete_in_thread=True
    )

    LINE_BUF = None
    LINE_MESSAGE = "< "

    print("Welcome to Heap.")
    print('Type ".help" for more information.')

    while True:

        keyword_completer.options = NestedCompleter.from_nested_dict(
            {
                **COMPLETE,
                **dict([(name, None) for name in runner.context["object"].keys()]),
            }
        ).options

        cmd = prompt.prompt(LINE_MESSAGE)
        cmd: str

        if cmd.strip()[-1] == "{" and LINE_MESSAGE == "< ":
            prompt.multiline = True
            LINE_MESSAGE = "↓ "
            LINE_BUF = cmd
            continue

        if LINE_MESSAGE == "↓ ":
            LINE_MESSAGE = "< "
            cmd = LINE_BUF + cmd
            prompt.multiline = False

        if cmd.strip() == "":
            continue

        if cmd.startswith("."):
            if cmd == ".exit":
                break
            elif cmd == ".help":
                ...
            else:
                print("> Bad command.")

            continue

        if cmd.strip()[-1] not in "};":
            cmd += ";"

        toks = lex(cmd).as_list()

        analyzer._toks = toks

        tree = analyzer.parse()
        runner.toks = tree

        val, type, _, __ = runner.run()

        if val != None:
            print(f"> {val}")
