from ..asts import Root, Func
from os import chdir, getcwd


def os_chdir(father: Root | Func, path):
    chdir(path)


def os_getcwd(father: Root | Func):
    return getcwd()


HEAP_EXPORT_FUNC = {"os_chdir": os_chdir, "os_getcwd": os_getcwd}
