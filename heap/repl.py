"""
一个简单的repl实现
"""


def repl():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import InMemoryHistory
    from .lexer import lex
    from .analyzer import Analyzer
    from .ast import ASTNode
    from .runner import Runner

    analyzer = Analyzer([])
    runner = Runner([])

    keyword_completer = WordCompleter(
        [
            "func",
            "var",
            "int",
            "string",
            "void",
            "float",
            "while",
            "return",
            "break",
            "continue",
        ]
    )

    prompt = PromptSession(completer=keyword_completer, history=InMemoryHistory())

    print("Welcome to Heap.")
    print('Type ".help" for more information.')

    while True:
        cmd = prompt.prompt("< ")
        cmd: str

        if cmd.strip() == "":
            continue

        if cmd.startswith("."):
            if cmd == ".exit":
                break

            else:
                print("> Bad command.")

            continue

        toks = lex(cmd).as_list()

        analyzer._toks = toks

        tree = analyzer.parse()
        runner.toks = tree

        val, type, _, __ = runner.run()

        if val != None:
            print(f"> {val}")
