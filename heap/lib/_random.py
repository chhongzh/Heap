# 随机模块
# chhongzh @ 2023

import random
from ..asts import Root, Func


def radint(father: Root | Func, a: int, b: int):
    return random.randint(a, b)
