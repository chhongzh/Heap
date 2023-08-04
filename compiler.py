from heap import Lexer, Builder, Runner
import click
from heap.loader import loader
from heap.compiler import Compiler
from os import chdir
from os.path import dirname


@click.command()
@click.argument("file")
@click.argument("output")
def main(file, output):
    print(
        "!!! 警告:编译器目前仍处于试验状态, 不保证编译后代码能成功运行. 编译后代码基于Native Python, 不应出现环境问题, 但是这将会把所有文件打包成单文件, 自行斟酌文件大小!. 建议Python3.9+运行. !!!"
    )
    print(f'准备编译:"{file}".')
    dt = loader(file)

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    root = b.parase()

    chdir(dirname(file))

    c = Compiler(root)
    fcontent = c.compile()

    with open(output, "w") as f:
        f.writelines(fcontent)

    print("编译完成")


if __name__ == "__main__":
    main()
