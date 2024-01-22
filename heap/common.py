# Heap @ 2024
# chhongzh

import sys as __sys
from os.path import join, split
from .const_value import DEEPTH

"""
一些公用函数
"""


def loader(path: str) -> str:
    """加载一个文件并返回内容"""

    with open(path, encoding="utf-8") as f:
        return f.read()


def crack_deepth() -> None:
    """设置最大递归深度"""

    __sys.setrecursionlimit(DEEPTH)


def make_shebang():
    cli_path = join(split(__file__)[0], "..", "cli.py")
    return " ".join([__sys.executable, cli_path, "run"])
