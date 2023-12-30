# 随机模块
# chhongzh @ 2023

import random
from ..asts import Root, Func


def random_randint(father: Root | Func, a: int, b: int):
    father.stack.append(random.randint(a, b))


def random_choice(father: Root | Func, lst: list):
    father.stack.append(random.choice(lst))
