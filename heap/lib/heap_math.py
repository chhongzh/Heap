"""
Heap标准库移植计划 - _math.py
移植Python3.11中的数学库至Heap

chhongzh @ 2023.8.10
"""

import math
from ..asts import Root, Func
from ..runner import Runner


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


def ceil(father: Root | Func, val):
    father.stack.append(math.ceil(val))


def floor(father: Root | Func, val):
    father.stack.append(math.floor(val))


def fabs(father: Root | Func, val):
    father.stack.append(math.fabs(val))


def gcd(father: Root | Func, val, val1):
    father.stack.append(math.gcd(val, val1))


def _heap_init(father: Root | Func):
    father.context["math_pi"] = math.pi


HEAP_EXPORT_FUNC = {
    "math_ceil": ceil,
    "math_cos": cos,
    "math_fabs": fabs,
    "math_floor": floor,
    "math_gcd": gcd,
    "math_getpi": getpi,
    "math_pow": pow,
    "math_sin": sin,
    "math_sqrt": sqrt,
}
