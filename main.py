from heap import Lexer, Builder, Runner
import click


@click.command()
@click.argument("file")
def main(file):
    with open(file) as f:
        dt = f.read()

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    root = b.parase()

    r = Runner(root)
    r.run()


if __name__ == "__main__":
    main()
