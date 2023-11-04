# Heap Lang repr实现
# chhongzh @ 2023.8.23
# 马上就要开学喽!
from heap.eprint import print_error


PRINT_BUFFER = []


class CatchError(Exception):
    pass


def _print(value):
    global PRINT_BUFFER
    PRINT_BUFFER.append(value)
    print(value, end="")


def print_and_stop(error):
    print_error(error)

    raise CatchError()


def repr() -> None:
    from locale import getlocale
    from os.path import dirname
    from os import getcwd, chdir

    from heap import Lexer, Builder, Runner
    from heap.asts import Root

    from heap import hook
    from heap.eprint import print_error

    from heap.error import InputError
    from heap.version_info import HEAP_VERSION_STR

    print(f"Heap Lang V{HEAP_VERSION_STR}")
    ln = 1  # 当前行数

    old = getcwd()

    hook._raise_error = print_error
    hook._print = _print

    # 上下文数据
    stack = []
    fn_ctx = {}
    var_ctx = {}
    command = {}

    while True:
        try:
            code = input("> ")
        except KeyboardInterrupt:
            print()
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

        hook._raise_error = print_and_stop

        l = Lexer(code)
        try:
            toks = l.lex()
        except CatchError:
            continue

        b = Builder(toks)

        try:
            ast_tree = b.parse()
        except CatchError:
            continue

        hook._raise_error = print_error

        ast_tree.stack = stack  # 上下文
        ast_tree.fn_ctx = fn_ctx  # 上下文
        ast_tree.var_ctx = var_ctx  # 上下文
        ast_tree.command = command  # 上下文

        r = Runner(ast_tree, old)
        r.run()

        # 自动换行:
        if len(PRINT_BUFFER) > 0 and str(PRINT_BUFFER[-1])[-1] != "\n":
            print("")

        del PRINT_BUFFER[:]  # 释放

        print(">", ast_tree.stack)  # 输出

        del l, b  # 清理
