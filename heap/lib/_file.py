# File操作

from ..asts import Func, Root
from ..log import info
from io import FileIO


def fileio_open(_: Func | Root, fname: str, mode: str, encoding):
    info(f"[Module]: [fileio]: 打开: fpath:{fname}, mode:{mode}, encoding:{encoding}")
    return open(fname, mode, encoding=encoding)


def fileio_close(_: Func | Root, file_io: FileIO):
    file_io.close()


def fileio_read(_: Func | Root, file_io: FileIO):
    return file_io.read()


def fileio_readlines(_: Func | Root, file_io: FileIO):
    return file_io.readlines()


def fileio_write(_: Func | Root, file_io: FileIO, data: str):
    file_io.write(data)
