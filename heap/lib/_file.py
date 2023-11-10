# File操作

from ..asts import Func, Root
from io import FileIO


def fileio_open(_: Func | Root, fname: str, mode: str, encoding):
    return open(fname, mode, encoding=encoding)


def fileio_close(_: Func | Root, file_io: FileIO):
    file_io.close()


def fileio_read(_: Func | Root, file_io: FileIO):
    return file_io.read()


def fileio_write(_: Func | Root, file_io: FileIO, data: str):
    file_io.write(data)
