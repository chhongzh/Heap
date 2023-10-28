# coding=utf-8
import click


@click.group()
def __wrapper():
    pass


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.argument("args", nargs=-1)
def run(filepath, args):
    from heap.loader import loader
    from heap import Lexer, Builder, Runner
    from os.path import dirname

    dt = loader(filepath)

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    root = b.parse()

    r = Runner(root, dirname(filepath))
    r.root.var_ctx["heap_argv"] = args
    r.run()


@__wrapper.command()
def repr():
    from heap.repr import repr

    repr()


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=False))
@click.argument("output")
def cppheap(filepath, output):
    from heap.cppheap.emitter import Emitter
    from heap.asts import Root
    from heap import Lexer, Builder
    from heap.loader import loader

    body = loader(filepath)

    l = Lexer(body)
    lex = l.lex()

    b = Builder(lex)
    r = b.parse()

    e = Emitter(r)

    a = e.emit()

    with open(output, "w") as f:
        f.writelines(a)


__wrapper()
