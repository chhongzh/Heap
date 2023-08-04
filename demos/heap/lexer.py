from .ops import OPS
from .token import Token
from .types import OBJ, ID, KEYWORD
from .keywords import KEYWORDS


class Lexer:
    def __init__(self, content: str):
        self.content = content
        self.pos = -1
        self.current = None
        self.tok = []

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.content):
            self.current = None
        else:
            self.current = self.content[self.pos]

    def lex(self):
        self.advance()

        while self.current:
            if self.current in OPS:
                self.tok.append(Token(OPS[self.current], self.current))
                self.advance()
            elif self.current == "[":
                self.tok.append(Token(OBJ, self.expr_list()))
                continue
            elif self.current == "#":
                self.advance()
                self.comment_match()
            elif self.current == '"':
                self.advance()
                self.tok.append(Token(OBJ, self.string_match()))
            elif self.number_check():
                self.tok.append(Token(OBJ, self.num_match()))
            elif self.current.isalpha():
                val = self.id_match()
                if val in KEYWORDS:
                    self.tok.append(Token(KEYWORD, val))
                else:
                    self.tok.append(Token(ID, val))
            else:
                self.advance()

        return self.tok

    def number_check(self):
        return self.isnum() or self.current == "-" or self.current == "."

    def string_match(self):
        cache = []
        while self.current and self.current != '"':
            cache.append(self.current)
            self.advance()
        self.advance()
        return "".join(cache).replace("\\n", "\n").replace("\\t", "\t")

    def is_num(self):
        self.current: str | None
        return self.current == "-" or self.current.isdecimal()

    def number_check(self):
        return self.isnum() or self.current == "-" or self.current == "."

    def isnum(self):
        return self.current.isdecimal()  # 使用isdigit会将部分非正常数字的unicode字符算入

    def num_match(self):
        is_negtive = False
        dot = False
        cache = []
        while self.current is not None and self.number_check():
            if self.current == "-":
                if is_negtive:
                    raise TypeError("Invalid negative.")
                else:
                    is_negtive = True
                    cache.append("-")
            elif self.isdot():
                if dot:
                    raise TypeError("Invalid dot.")
                else:
                    dot = True
                    cache.append(".")
            elif self.isnum():
                cache.append(self.current)
            else:
                raise TypeError("Invalid number.")

            self.advance()
        if "." in cache:
            return float("".join(cache))
        else:
            return int("".join(cache))

    def isdot(self):
        return self.current == "."

    def id_match(self):
        from .ops import OPS

        cache = []
        while self.current:
            if self.current in OPS or self.current in (" ", "\n"):
                break

            cache.append(self.current)
            self.advance()

        return "".join(cache)

    def comment_match(self):
        lst = ["\n", "#"]
        while self.current and self.current not in lst:
            self.advance()
        self.advance()

    def expr_list(self):
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
                raise Exception
            else:
                self.advance()

        self.advance()  # skip ]

        return cache
