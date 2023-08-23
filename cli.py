import click


@click.group()
def __wrapper():
    pass


@__wrapper.command()
@click.argument("filepath", type=click.Path(exists=True))
def run(filepath):
    from heap.loader import loader
    from heap import Lexer, Builder, Runner
    from os.path import dirname

    dt = loader(filepath)

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    root = b.parase()

    r = Runner(root, dirname(filepath))
    r.run()


@__wrapper.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path(exists=False))
def compile(input_filepath, output_filepath):
    from heap.loader import loader
    from os import getcwd, chdir
    from os.path import dirname
    from heap import Compiler, Lexer, Builder

    old_dir = getcwd()

    dt = loader(input_filepath)
    chdir(dirname(input_filepath))

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    tree = b.parase()

    c = Compiler(tree)
    fcontent = c.compile()

    chdir(old_dir)

    with open(output_filepath, "w") as f:
        f.writelines(fcontent)


@__wrapper.command()
def repr():
    from heap.cli import repr

    repr()


__wrapper()
