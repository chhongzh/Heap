# Heap @ 2023
# chhongzh

"""输出错误的模块"""

from .error import BaseError


def print_error(error: BaseError):
    """用于输出一个错误"""
    print(
        f"Encountered an error -> {error.__class__.__name__} ->"
        f" Token:{error.val}, Pos:{error.pos}, {error.args};"
    )
