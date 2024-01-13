# chhongzh @ 2024
# Heap - 标准库 - time(时间)

"""
部分时间函数
"""

from ..asts import Root
from time import time, sleep


def time_time(_: Root):
    return time()


def time_sleep(_: Root, ns):
    sleep(ns)


HEAP_EXPORT_FUNC = {
    "time_sleep": time_sleep,
    "time_time": time_time,
}
