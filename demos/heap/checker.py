from .types import KEYWORD
from . import Lexer
from .token import Token

MESSAGE = {
    "redundant func": "多余的endfunc关键字",
    "unclosed func": "没有关闭的func标签",
    "redundant command": "多余的endcommand关键字",
    "unclosed command": "没有关闭的command标签",
    "not int": "不是个数字",
    "": "",
}


def syntax_check(text: str):
    lexer = Lexer(text)
    try:
        toks = lexer.lex()
    except ValueError:
        return "not int", -1

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
                    return "redundant func", pos
            elif tok.value == "command":
                command_level += 1
            elif tok.value == "endcommand":
                command_level -= 1

                if command_level < 0:
                    return "redundant command", pos

    if func_level > 0:
        return "unclosed func", -1
    if command_level > 0:
        return "unclosed command", -1

    return "", -1
