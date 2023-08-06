from .types import KEYWORD
from . import Lexer
from .token import Token

MESSAGE = {
    "未打开func": "多余的endfunc关键字",
    "未关闭func": "没有关闭的func标签",
    "未打开command": "多余的endcommand关键字",
    "未关闭command": "没有关闭的command标签",
    "不是数字": "不是个数字",
    "": "",
}


def syntax_check(text: str):
    lexer = Lexer(text)
    try:
        toks = lexer.lex()
    except ValueError:
        return "不是数字", -1

    toks: list[Token]
    pos = -1

    func_level = 0
    command_level = 0

    for tok in toks:
        pos += 1
        if tok.type == KEYWORD:
            if tok.value == "func":
                func_level += 1
            elif tok.value == "endfunc":
                func_level -= 1

                if func_level < 0:
                    return "未打开func", pos
            elif tok.value == "command":
                command_level += 1
            elif tok.value == "endcommand":
                command_level -= 1

                if command_level < 0:
                    return "未打开command", pos

    if func_level > 0:
        return "未关闭func", -1
    if command_level > 0:
        return "未关闭command", -1

    return "", -1
