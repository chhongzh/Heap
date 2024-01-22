#!python3
# coding=utf-8

"""
Heap @ 2023

这是一个基于Python开发的编程语言, 使用Python3.11开发

你可以在https://github.com/chhongzh/Heap查看更多信息
"""
import click

from heap import Lexer, Builder, Runner
from heap.repl import heap_repl
from heap import loader
from heap.common import crack_deepth
from heap.heapb import loader as byte_loader
from heap.heapb import writer as byte_writer
from heap.version_info import HEAP_VERSION_STR
from sys import platform as SYS_PLATFORM
from pathlib import Path

# !!! 防止递归深度
crack_deepth()

# 加强输入
if SYS_PLATFORM != "win32":
    import readline

try:
    from heap.compile_info import IS_COMPILE, COMPILE_DATE
except ModuleNotFoundError:
    IS_COMPILE = False
    COMPILE_DATE = None

from heap.log import HEAP_IO
from os.path import dirname


@click.group()
@click.version_option(
    version=f"{HEAP_VERSION_STR} (Not compile.)"
    if not IS_COMPILE
    else f"{HEAP_VERSION_STR} (Compiled on {COMPILE_DATE}.)",
    prog_name="Heap",
)
def __wrapper():
    pass


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--showlog", default=False, is_flag=True)
@click.argument("args", nargs=-1)
def run(filepath, showlog, args):
    """
    运行Heap程序
    """

    is_byte = ".heapb" == Path(filepath).suffix

    if not is_byte:  # Normal File mode
        dt = loader(filepath)

        l = Lexer(dt)
        toks = l.lex()

        b = Builder(toks, filepath)
        root = b.parse()

    else:
        root = byte_loader(filepath)

    r = Runner(root, dirname(filepath))
    r.root.context["heap_argv"] = args
    r.run()

    if showlog:
        print(HEAP_IO.getvalue(), end="")


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.argument("outputpath", type=click.Path())
def build(filepath, outputpath):
    dt = loader(filepath)

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks, filepath)
    root = b.parse()

    byte_writer(root, f"{outputpath}.heapb")


@__wrapper.command()
def repl():  # pylint:disable=W0622
    """REPL环境"""
    heap_repl()


__wrapper()
