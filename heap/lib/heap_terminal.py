# Heap
# chhongzh @ 2023

# 获取终端大小
from ..asts import Root, Func
import os


def get_terminal_size(father: Root | Func):
    x, y = os.get_terminal_size()
    father.stack.append(x)
    father.stack.append(y)


HEAP_EXPORT_FUNC = {
    "get_terminal_size": get_terminal_size,
}
