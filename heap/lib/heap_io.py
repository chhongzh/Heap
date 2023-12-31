# File操作

from ..asts import Func, Root
from ..log import info
from io import FileIO


def io_close(_: Func | Root, file_io: FileIO):
    file_io.close()


def io_read(_: Func | Root, file_io: FileIO):
    return file_io.read()


def io_readlines(_: Func | Root, file_io: FileIO):
    return file_io.readlines()


def io_write(_: Func | Root, file_io: FileIO, data: str):
    file_io.write(data)


def io_readline(_: Func | Root, file_io: FileIO):
    return file_io.readline()


def io_flush(_: Func | Root, file_io: FileIO):
    file_io.flush()


def io_fileno(_: Func | Root, file_io: FileIO):
    return file_io.fileno()


def io_readable(_: Func | Root, file_io: FileIO):
    return file_io.readable()


def io_isatty(_: Func | Root, file_io: FileIO):
    return file_io.isatty()


def io_writable(_: Func | Root, file_io: FileIO):
    return file_io.writable()


def io_writelines(_: Func | Root, file_io: FileIO):
    file_io.writelines()


def io_tell(_: Func | Root, file_io: FileIO):
    return file_io.tell()


def io_seek(_: Func | Root, file_io: FileIO, p: int):
    return file_io.seek(p)


def io_seekable(_: Func | Root, file_io: FileIO):
    return file_io.seekable()
