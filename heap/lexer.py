# Heap @ 2023
# chhongzh

"""
Heap的Lexer
"""

from .ops import OPS
from .token import MetaInfo, Token
from .types import EQUAL, OBJ, ID, KEYWORD, LINK
from .keywords import KEYWORDS
from . import hook
from .error import LexerError, SyntaxErr
from .log import info


class Lexer:
    """Heap 分词器"""

    def __init__(self, content: str):
        self.content = content
        self.pos = -1
        self.line_no = 1
        self.current = None
        self.tok = []

        self.id_range = [
            *list("abcdefghijklmnopqrstuvwxyz"),
            *list("abcdefghijklmnopqrstuvwxyz".upper()),
            *list("1234567890_"),
        ]

        info("[Lexer]: 就绪")

    def advance(self):
        """下一个字符"""

        self.pos += 1
        if self.pos >= len(self.content):
            self.current = None
        else:
            self.current = self.content[self.pos]

    def lex(self):
        """分词"""

        info("[Lexer]: 开始分词")

        self.advance()

        while self.current:
            if self.current in OPS:
                self.tok.append(
                    Token(
                        OPS[self.current],
                        self.current,
                        MetaInfo(self.pos, self.pos, self.line_no),
                    )
                )
                self.advance()
            elif self.current == "[":
                temp_pos = self.pos
                self.tok.append(
                    Token(
                        OBJ,
                        self.expr_list(),
                        MetaInfo(temp_pos, temp_pos, self.line_no),
                    )
                )

            elif self.current == "#":
                self.advance()
                self.comment_match()
            elif self.current == "-":
                self.advance()
                if self.current == ">":
                    self.tok.append(
                        Token(LINK, "->", MetaInfo(self.pos, self.pos, self.line_no))
                    )
                    self.advance()
            elif self.current == '"':
                self.advance()

                start_pos = self.pos
                data = self.string_match()
                end_pos = self.pos

                self.tok.append(
                    Token(OBJ, data, MetaInfo(start_pos, end_pos, self.line_no))
                )
            elif self.number_check():
                start_pos = self.pos
                data = self.num_match()
                end_pos = self.pos
                self.tok.append(
                    Token(OBJ, data, MetaInfo(start_pos, end_pos, self.line_no))
                )
            elif self.current.isalpha():
                start_pos = self.pos

                val = self.id_match()
                if val in KEYWORDS:
                    self.tok.append(
                        Token(
                            KEYWORD,
                            val,
                            MetaInfo(start_pos, start_pos + len(val), self.line_no),
                        )
                    )
                else:
                    self.tok.append(
                        Token(
                            ID,
                            val,
                            MetaInfo(
                                start_pos,
                                start_pos + len(val) if val else 0,
                                self.line_no,
                            ),
                        )
                    )
            elif self.current == "=":
                self.tok.append(self.match_equal())
            else:
                if self.current == "\n":
                    self.line_no += 1
                self.advance()

        info(f"[Lexer]: 分词完成 (Toks cnt:{len(self.tok)})")

        return self.tok

    def match_equal(self):
        buf = []
        equal_tok = ["=", "<", ">", "!"]

        while self.current in equal_tok:
            buf.append(self.current)
            self.advance()

        if len(buf) not in (1, 2):
            hook.print_error(SyntaxErr(f'未知的"="语法定义.', self.pos))

        if len(buf) == 1:
            tok = buf[0]

            if tok == "=":
                return Token(EQUAL, "=", MetaInfo(self.pos, self.pos, self.line_no))
            else:
                hook.print_error(SyntaxErr(f"", -1))

    def string_match(self):
        "匹配字符串"

        cache = []
        while self.current and self.current != '"':
            if self.current == "\\":
                self.advance()
                match self.current:
                    case "n":
                        cache.append("\n")
                    case "t":
                        cache.append("\t")
                    case '"':
                        cache.append('"')
                    case "r":
                        cache.append("\r")
                    case "a":
                        cache.append("\a")
                    case "b":
                        cache.append("\b")
                    case _:
                        hook.raise_error(
                            LexerError(f"\\{self.current}", self.pos, "未知的转义")
                        )
                self.advance()
                continue
            cache.append(self.current)
            self.advance()
        self.advance()
        return "".join(cache)

    def is_num(self):
        """判断是否是数字"""

        self.current: str | None
        return self.current == "-" or self.current.isdecimal()

    def number_check(self):
        """判断是否是数字部分"""

        return self.isnum() or self.current == "-" or self.current == "."

    def isnum(self):
        "检查是否是数字"

        return self.current.isdecimal()  # 使用isdigit会将部分非正常数字的unicode字符算入

    def num_match(self):
        """数字匹配"""

        is_negtive = False
        dot = False
        cache = []
        while self.current is not None and self.number_check():
            if self.current == "-":
                if is_negtive:
                    hook.raise_error(LexerError("", self.pos, "Invalid negative."))
                else:
                    is_negtive = True
                    cache.append("-")
            elif self.isdot():
                if dot:
                    hook.raise_error(LexerError("", self.pos, "Invalid dot."))
                else:
                    dot = True
                    cache.append(".")
            elif self.isnum():
                cache.append(self.current)
            else:
                hook.raise_error(LexerError("", self.pos, "Invalid number."))

            self.advance()
        if "." in cache:
            try:
                return float("".join(cache))
            except:
                hook.raise_error(LexerError("未知的float.", self.pos, "".join(cache)))
        return int("".join(cache))

    def isdot(self):
        """判断当前是否为."""

        return self.current == "."

    def id_match(self):
        """解析ID"""

        cache = []
        while self.current:
            if not ("\u4e00" <= self.current <= "\u9fff") and (
                self.current not in self.id_range
            ):
                break

            cache.append(self.current)
            self.advance()

        k = "".join(cache)

        if k == "null":
            return None

        return k

    def comment_match(self):
        """解析注释"""

        lst = ["\n", "#"]
        while self.current and self.current not in lst:
            self.advance()
        self.advance()

    def expr_list(self):
        """解析列表"""

        self.advance()  # skip [

        cache = []

        while self.current != "]":
            if self.current == "[":
                cache.append(self.expr_list())

            elif self.current == "#":
                self.advance()
                self.comment_match()
            elif self.current == '"':
                self.advance()
                cache.append(self.string_match())
            elif self.number_check():
                cache.append(self.num_match())
            elif self.current.isalpha():
                hook.raise_error(LexerError(self.current, self.pos, "列表不应该出现id"))
            else:
                self.advance()

        self.advance()  # skip ]

        return cache
