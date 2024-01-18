# Heap @ 2024
# chhongzh

import sys as __sys
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
