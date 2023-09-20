# Heap Lang repr实现
# chhongzh @ 2023.8.23
# 马上就要开学喽!

PRINT_BUFFER = []


def _print(value):
    global PRINT_BUFFER
    PRINT_BUFFER.append(value)
    print(value, end="")


def repr() -> None:
    from locale import getlocale
    from os.path import dirname
    from os import getcwd, chdir

    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style

    from heap import Lexer, Builder, Runner
    from heap.asts import Root

    from heap import hook
    from heap.eprint import print_error

    from heap.error import InputError

    print("Heap Lang")
    session = PromptSession()
    ln = 1  # 当前行数

    old = getcwd()

    hook._raise_error = print_error
    hook._print = _print

    # 上下文数据
    stack = []
    fn_ctx = {}
    var_ctx = {}
    command = {}

    style = Style.from_dict(
        {
            "rprompt": "bg:#CCCCCC #000000",
        }
    )

    def rprompt():
        return f"{ln}"

    while True:
        try:
            code = session.prompt(
                "< ",
                rprompt=rprompt,
                style=style,
                mouse_support=True,
            )
        except KeyboardInterrupt:
            hook._raise_error(InputError("stdin", 0))
            continue

        code: str  # 类型注解

        if code.strip() == "":
            # 如果空直接跳过
            continue

        ln += 1
        if code == "exit":
            # 退出
            break

        l = Lexer(code)
        toks = l.lex()

        b = Builder(toks)
        ast_tree = b.parse()

        ast_tree.stack = stack  # 上下文
        ast_tree.fn_ctx = fn_ctx  # 上下文
        ast_tree.var_ctx = var_ctx  # 上下文
        ast_tree.command = command  # 上下文

        r = Runner(ast_tree, old)
        r.run()

        # 自动换行:
        if len(PRINT_BUFFER) > 0 and PRINT_BUFFER[-1][-1] != "\n":
            print("")

        del PRINT_BUFFER[:]  # 释放

        print(">", ast_tree.stack)  # 输出

        del l, b  # 清理
