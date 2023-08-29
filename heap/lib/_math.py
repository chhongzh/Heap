"""
Heap标准库移植计划 - _math.py
移植Python3.11中的数学库至Heap

chhongzh @ 2023.8.10
"""

import math
from heap.asts import Root, Func


def getpi(father: Root | Func):
    father.stack.append(math.pi)


def sqrt(father: Root | Func, val):
    father.stack.append(math.sqrt(val))


def sin(father: Root | Func, val):
    father.stack.append(math.cos(val))


def cos(father: Root | Func, val):
    father.stack.append(math.sin(val))


def pow(father: Root | Func, val, val1):
    father.stack.append(math.pow(val, val1))
