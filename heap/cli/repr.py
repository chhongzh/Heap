# Heap Lang repr实现
# chhongzh @ 2023.8.23
# 马上就要开学喽!


def repr() -> None:
    from heap.ui.i18n import i18n
    from locale import getlocale
    from os.path import dirname
    from os import getcwd, chdir

    old = getcwd()  # 获得当前工作目录
    chdir(dirname(__file__))

    from rich.console import Console
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style

    from heap import Lexer, Builder, Runner
    from heap.asts import Root

    from heap import hook
    from heap.eprint import print_error

    from heap.error import InputError

    from heap.checker import syntax_check, MESSAGE

    i = i18n(f"heap/lang/{getlocale()[0]}.json", "heap/lang/zh_CN.json")  # 加载语言

    t = i.t

    c = Console()
    c.print(t("解释器.版本信息"), highlight=False)
    session = PromptSession()
    ln = 1  # 当前行数

    hook._raise_error = print_error

    # 上下文数据
    stack = []
    fn_ctx = {}
    var_ctx = {}
    command = {}

    style = Style.from_dict(
        {
            "rprompt": "bg:#CCCCCC #000000",
        }
    )

    def bottom_tool_bar():
        if session.default_buffer.document.text == "exit":
            return t("解释器.提示框.退出")
        err, pos = syntax_check(session.default_buffer.document.text)
        if err:
            return t(f"解释器.错误消息.{err}")
        else:
            return t("解释器.提示框.信息")

    def rprompt():
        return f"{ln}"

    chdir(old)  # 加载完成后切回

    while True:
        try:
            code = session.prompt(
                "< ",
                bottom_toolbar=bottom_tool_bar,
                rprompt=rprompt,
                style=style,
                mouse_support=True,
            )
        except KeyboardInterrupt:
            hook._raise_error(InputError("stdin", 0))
            continue

        code: str  # 类型注解

        if code.strip() == "":
            # 如果空直接跳过
            continue

        ln += 1
        if code == "exit":
            # 退出
            break

        l = Lexer(code)
        toks = l.lex()

        b = Builder(toks)
        ast_tree = b.parse()

        ast_tree.stack = stack  # 上下文
        ast_tree.fn_ctx = fn_ctx  # 上下文
        ast_tree.var_ctx = var_ctx  # 上下文
        ast_tree.command = command  # 上下文

        r = Runner(ast_tree, old)
        r.run()

        print(">", ast_tree.stack)  # 输出

        del l, b  # 清理
