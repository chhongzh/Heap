# chhongzh @ 2023
# Heap - 标准库 - TOML

"""
提供部分Toml支持
"""

from tomllib import loads
from ..asts import Func, Root


def toml_loads(father: Root | Func, s: str):
    return loads(s)


HEAP_EXPORT_FUNC = {
    "toml_loads": toml_loads,
}
