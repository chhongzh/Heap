#coding=utf-8
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
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path(exists=False))
def transpile(input_filepath, output_filepath):
    from heap.loader import loader
    from os import getcwd, chdir
    from os.path import dirname
    from heap import Transpiler, Lexer, Builder

    old_dir = getcwd()

    dt = loader(input_filepath)
    chdir(dirname(input_filepath))

    l = Lexer(dt)
    toks = l.lex()

    b = Builder(toks)
    tree = b.parse()

    c = Transpiler(tree)
    fcontent = c.compile()

    chdir(old_dir)

    with open(output_filepath, "w") as f:
        f.writelines(fcontent)


@__wrapper.command()
def repr():
    from heap.cli import repr

    repr()


@__wrapper.group()
def heapack():
    """Heap默认的包管理器"""
    print("Heap Package Manager.")


@heapack.command()
@click.argument("output", type=click.Path())
def pack(output: str):
    """打包当前目录"""
    from heap.heapack import Packer
    from prompt_toolkit.shortcuts import input_dialog, radiolist_dialog, message_dialog
    from heap.heapack.check import check_package_name, check_version
    from os import getcwd

    print(f"目录为:{getcwd()}")
    p = Packer(".", output + ".heapack")

    # 读取Name
    name = input_dialog("heapack", "输入名称").run()
    if name is None:
        print("heapack: 用户取消")
        return

    # 读取Package Name
    package_name = input_dialog("heapack", "输入包名").run()
    if package_name is None:
        print("heapack: 用户取消")
        return
    if not check_package_name(package_name):
        print("heapack: 错误的包名")
        return

    # 读取版本
    version = input_dialog("heapack", "输入版本(x.x.x)").run()
    if version is None:
        print("heapack: 用户取消")
        return
    if not check_version(version):
        print("heapack: 错误版本")
        return
    version = map(int, version.split("."))

    # 读取作者
    authors = []
    while True:
        author = input_dialog("heapack", "输入作者(留空完成)").run()
        if author == "" or author is None:
            if len(authors) <= 0:
                message_dialog("heapack", "至少需要一个作者").run()
                continue
            break

        authors.append(author)

    # 读取依赖
    requires = []
    while True:
        require = input_dialog("heapack", "输入require(留空完成)").run()
        if require == "" or require is None:
            break

        requires.append(require)

    p.set_name(name).set_package(package_name).set_version(version).set_authors(
        authors
    ).set_require(requires).pack()


@heapack.command()
@click.argument("file")
def unpack(file):
    from heap.heapack import Unpacker

    u = Unpacker(".", file)

    u.install()


__wrapper()
