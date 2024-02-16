#!python3
# coding=utf-8

"""
Heap @ 2024

Heap V2, 
New heights, better than Heap V1.
"""
import click

from heap import lex
from heap import reader
from heap.analyzer import Analyzer
from heap.runner import Runner
from heap.compiler import compile_from_builded_ast
from sys import platform as SYS_PLATFORM


# 加强输入
if SYS_PLATFORM != "win32":
    import readline

try:
    from heap.compile_info import IS_COMPILE, COMPILE_DATE
except ModuleNotFoundError:
    IS_COMPILE = False
    COMPILE_DATE = None


@click.group()
@click.version_option(
    version=(
        f"Heap V2 (Not compile.)"
        if not IS_COMPILE
        else f"HEAP V2 (Compiled on {COMPILE_DATE}.)"
    ),
    prog_name="Heap",
)
def __wrapper():
    pass


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
# @click.argument("args", nargs=-1)
def run(filepath):
    fdata = reader(filepath)
    toks = lex(fdata).as_list()

    a = Analyzer(toks)
    tree = a.parse()
    r = Runner(tree)
    r.run()


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
def compile(filepath):
    fdata = reader(filepath)
    toks = lex(fdata).as_list()

    a = Analyzer(toks)
    tree = a.parse()
    compile_from_builded_ast(
        tree, cpp_path=filepath + ".cpp", binary_path=filepath + ".out"
    )


__wrapper()
