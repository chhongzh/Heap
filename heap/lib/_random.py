# 随机模块
# chhongzh @ 2023

import random
from ..asts import Root, Func


def randint(father: Root | Func, a: int, b: int):
    father.stack.append(random.randint(a, b))
