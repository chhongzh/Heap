# Heap @ 2023
# chhongzh

"""输出错误的模块"""

from .error import BaseError


def print_error(error: BaseError):
    """用于输出一个错误"""

    pos_message = "" if error.pos == -1 else f", Pos:{error.pos}"
    error_message = "" if not error.args else f", {''.join(error.args)}"

    print(
        f"Encountered an error -> {error.__class__.__name__} ->"
        f" Token:{error.val}{pos_message}{error_message};"
    )
