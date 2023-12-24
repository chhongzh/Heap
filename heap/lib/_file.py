# File操作

from ..asts import Func, Root
from ..log import info
from io import FileIO


def file_open(_: Func | Root, fname: str, mode: str, encoding):
    info(f"[Module]: [fileio]: 打开: fpath:{fname}, mode:{mode}, encoding:{encoding}")
    return open(fname, mode, encoding=encoding)
