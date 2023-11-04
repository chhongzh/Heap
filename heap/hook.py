# Heap @ 2023
# chhongzh

"Heap的钩子"

import sys
from .eprint import print_error


def print_val(val):
    "print钩子"

    print(val, end="")


def raise_error(error):
    "抛出错误并退出"

    print_error(error)

    sys.exit(1)
