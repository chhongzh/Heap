# coding=utf-8

"""
Heap @ 2023

这是一个基于Python开发的编程语言, 使用Python3.11开发

你可以在https://github.com/chhongzh/Heap查看更多信息
"""
from os.path import dirname
import click

from heap import Lexer, Builder, Runner
from heap.repr import heap_repr
from heap.loader import loader

from heap.log import HEAP_IO


@click.group()
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

    dt = loader(filepath)

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    root = b.parse()

    r = Runner(root, dirname(filepath))
    r.root.var_ctx["heap_argv"] = args
    r.run()

    if showlog:
        print(HEAP_IO.getvalue(), end="")


@__wrapper.command()
def repr():  # pylint:disable=W0622
    """REPR环境"""
    heap_repr()


__wrapper()
