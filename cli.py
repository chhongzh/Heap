from heap.ui.i18n import i18n

from rich.console import Console
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.styles import Style

from heap import Lexer, Builder, Runner
from heap.asts import Root

from heap import hook
from heap.interpreter import _print
from heap.eprint import print_error

from heap.error import InputError

from heap.checker import syntax_check, MESSAGE

i = i18n("heap/lang/zh_cn.json", "heap/lang/zh_CN.json")

t = i.t

c = Console()
c.print(t("解释器.版本信息"), highlight=False)
session = PromptSession()
ln = 1

hook._raise_error = print_error

stack = []
fn_ctx = {}
var_ctx = {}
command = {}

example_style = Style.from_dict(
    {
        "rprompt": "bg:#CCCCCC #000000",
    }
)


def bottom_tool_bar():
    if session.default_buffer.document.text == "exit":
        return t("解释器.提示框.退出")
    err, pos = syntax_check(session.default_buffer.document.text)
    if err:
        return f"位于:{pos},存在{MESSAGE[err]}问题. "
    else:
        return t("解释器.提示框.信息")


def rprompt():
    return f"{ln}"


while True:
    try:
        code = session.prompt(
            "< ",
            bottom_toolbar=bottom_tool_bar,
            rprompt=rprompt,
            style=example_style,
            mouse_support=True,
        )
    except KeyboardInterrupt:
        hook._raise_error(InputError("stdin", 0))
        continue

    if code.strip() == "":
        continue

    ln += 1
    if code == "exit":
        break

    l = Lexer(code)
    toks = l.lex()

    b = Builder(toks)
    ast_tree = b.parase()

    ast_tree.stack = stack  # 钩子
    ast_tree.fn_ctx = fn_ctx  # 钩子
    ast_tree.var_ctx = var_ctx  # 钩子
    ast_tree.command = command  # 钩子

    r = Runner(ast_tree)
    r.run()

    print(">", ast_tree.stack)
    # print(">", ast_tree.fn_ctx)
    # print(">", ast_tree.var_ctx)

    del l, b
