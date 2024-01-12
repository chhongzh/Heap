# chhongzh @ 2024
# heap - 标准库 - ios

"""
IOS - Io Super.

包含了部分增强IO
"""

from io import StringIO
from ..asts import Func, Root


def ios_stringio(_: Root | Func):
    return StringIO()


def ios_getvalue(_: Root | Func, io: StringIO):
    return io.getvalue()


HEAP_EXPORT_FUNC = {"ios_stringio": ios_stringio, "ios_getvalue": ios_getvalue}
