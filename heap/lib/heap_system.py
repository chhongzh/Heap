# 系统模块
# chhongzh @ 2023

from ..asts import Root, Func
from .. import Lexer, Builder, Runner
import sys


def exec(father: Root | Func, raw_code: str):
    # 这个函数很危险, 应该在确保输入时安全时执行.

    l = Lexer(raw_code).lex()

    b = Builder(l).parse()

    father.runner.visits(b.body, father)


def system_get_stdout(_):
    return sys.stdout


def system_set_stdout(_: Root | Func, stdout):
    sys.stdout = stdout


HEAP_EXPORT_FUNC = {
    "system_exec": exec,
    "system_get_stdout": system_get_stdout,
    "system_set_stdout": system_set_stdout,
}
