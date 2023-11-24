# Heap Lang repr实现
# chhongzh @ 2023.8.23
# 马上就要开学喽!

"""Heap repr"""

from os import getcwd
from heap import Lexer, Builder, Runner
from heap import hook
from heap.eprint import print_error
from heap.error import InputError
from heap.version_info import HEAP_VERSION_STR
from heap.log import info


NEED_PRINT_NEW_LINE = False
info("[REPR]: Repr mode is on.")
info("[REPR]: Inject and hook the function.")


class CatchError(Exception):
    pass


def _print(value):
    """输出并缓存到BUFFER"""

    global NEED_PRINT_NEW_LINE
    NEED_PRINT_NEW_LINE = str(value)[-1] != "\n"
    print(value, end="")


def print_and_stop(error):
    """输出并抛出错误"""

    print_error(error)

    raise CatchError()


def heap_repr() -> None:
    """Heap repr主函数"""

    info("[REPR]: OK to init. Ready for input.")

    NEED_PRINT_NEW_LINE = False

    print(f"Heap Lang V{HEAP_VERSION_STR}")
    print('Type "exit;" to exit. "help;" to watch help.')
    ln = 1  # 当前行数

    old = getcwd()

    hook.raise_error = print_error
    hook.print_val = _print

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
            hook.raise_error(InputError("stdin", 0))
            continue

        code: str  # 类型注解

        if code.strip() == "":
            # 如果空直接跳过
            continue

        ln += 1
        if code == "exit;":
            # 退出
            break

        hook.raise_error = print_and_stop

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

        hook.raise_error = print_error

        ast_tree.stack = stack  # 上下文
        ast_tree.fn_ctx = fn_ctx  # 上下文
        ast_tree.var_ctx = var_ctx  # 上下文
        ast_tree.command = command  # 上下文

        r = Runner(ast_tree, old)
        r.run()

        # 自动换行:
        if NEED_PRINT_NEW_LINE:
            print()
            NEED_PRINT_NEW_LINE = False  # 释放

        print(">", ast_tree.stack)  # 输出

        del l, b  # 清理
