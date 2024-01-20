# Heap Lang repr实现
# chhongzh @ 2023.8.23
# 马上就要开学喽!

"""Heap repr"""

from os import getcwd
from . import Lexer, Builder, Runner, multiline_input
from . import hook
from .error_printer import print_error
from .error import InputError
from .version_info import HEAP_VERSION_STR
from .log import info


NEED_PRINT_NEW_LINE = False
FIRST_RUN = True
info("[REPL]: Repr mode is on.")
info("[REPL]: Inject and hook the function.")


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


def heap_repl() -> None:
    """Heap repl主函数"""

    info("[REPL]: OK to init. Ready for input.")

    global NEED_PRINT_NEW_LINE, FIRST_RUN

    print(f"Heap Lang V{HEAP_VERSION_STR}")
    print('输入 "exit;" 来退出. "help;" 来查看帮助. "\'" 启用多行输入(再次输入则关闭多行输入).')
    ln = 1  # 当前行数

    old = getcwd()

    hook.raise_error = print_error
    hook.print_val = _print

    # 上下文数据
    stack = []
    var_ctx = {}
    command = {}

    while True:
        try:
            code = input("< ")
        except KeyboardInterrupt:
            print()
            hook.raise_error(InputError("stdin", 0))
            continue

        code: str  # 类型注解

        if code.strip() == "":
            # 如果空直接跳过
            continue

        if code == "exit;":
            # 退出
            break
        elif code == "'":
            # 多行输入模式:
            code = "\n".join(multiline_input.multiline_input())

        hook.raise_error = print_and_stop

        l = Lexer(code)
        try:
            toks = l.lex()
        except CatchError:
            continue

        b = Builder(toks, "stdin")

        try:
            ast_tree = b.parse()
        except CatchError:
            if code == "exit":
                print('> TIPS: 您看起来好像缺少了";", 若想退出REPL, 输入"exit;"')
            continue

        ast_tree.stack = stack  # 上下文
        ast_tree.context = var_ctx  # 上下文
        ast_tree.command = command  # 上下文

        should_inject_lib = not bool(ln - 1)  # 非零即真, ln 默认为 1 , 所以为 True
        r = Runner(ast_tree, old, should_inject_lib, var_ctx)

        try:
            r.run()
        except CatchError:
            continue

        hook.raise_error = print_error

        # 自动换行:
        if NEED_PRINT_NEW_LINE:
            print()
            NEED_PRINT_NEW_LINE = False  # 释放

        print(">", ast_tree.stack)  # 输出

        var_ctx = r.root.context

        del l, b  # 清理

        ln += 1
