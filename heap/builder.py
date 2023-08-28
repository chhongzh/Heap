from .stdlibs import LIBS
from .token import Token
from .asts import (
    Command,
    Div,
    Mul,
    Replace,
    Root,
    Func,
    Set,
    Get,
    Print,
    Add,
    Push,
    Call,
    Return,
    Sub,
    If,
    Include,
    Pop,
    Input,
    Try,
    While,
)
from .types import OBJ, SEM, VARDEF, KEYWORD, REPLACE, ID, COLON
from .keywords import KEYWORDS
from os.path import exists
from . import hook
from .error import ERRDICT


class Builder:
    def __init__(self, toks: list[Token]):
        self.toks = toks
        self.pos = -1
        self.tok = None
        self.root = []

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.toks):
            self.tok = None
        else:
            self.tok = self.toks[self.pos]

    def parse(self):
        self.advance()
        while self.tok:
            self.root.append(self.expr())
        return Root(self.root)

    def expr(self):
        if self.tok.type == KEYWORD:
            if self.tok.value == "func":
                t = self.match_fn()
                return t
            elif self.tok.value == "div":
                self.advance()
                self.advance()

                return Div()
            elif self.tok.value == "mul":
                self.advance()
                self.advance()

                return Mul()
            elif self.tok.value == "set":
                t = self.match_set()
                self.advance()  # SEM
                return t
            elif self.tok.value == "get":
                t = self.match_get()
                self.advance()
                return t
            elif self.tok.value == "push":
                t = self.match_push()
                self.advance()  # SEM

                return t
            elif self.tok.value == "print":
                self.advance()  # PRINT
                self.advance()  # SEM

                return Print()
            elif self.tok.value == "add":
                self.advance()  # ADD
                self.advance()  # SEM

                return Add()
            elif self.tok.value == "pop":
                self.advance()  # pop
                self.advance()  # SEM

                return Pop()
            elif self.tok.value == "sub":
                self.advance()  # SUB
                self.advance()  # SEM

                return Sub()
            elif self.tok.value == "return":
                self.advance()  # RETURN
                t = self.match_return()

                return t
            elif self.tok.value == "while":
                return self.match_while()
            elif self.tok.value == "if":
                print(self.tok.value)
                return self.match_if()
            elif self.tok.value == "include":
                return self.match_include()
            elif self.tok.value == "command":
                return self.match_command()
            elif self.tok.value == "input":
                self.advance()  # Input
                title = Replace if self.tok.type == REPLACE else self.tok.value
                self.advance()  # title
                self.advance()  # sem
                return Input(title)
        elif self.tok.type == ID:
            return self.match_call()

        self.catch_error()
        self.advance()
        # raise Exception("Unknow", self.tok, self.pos)

    def match_if(self):
        l1s = []
        ops = []
        l2s = []
        bodys = []

        while self.tok.value != "endif":
            l1, op, l2, body = self.if_const()
            if None not in (l1, op, l2):
                l1s.append(l1)
                ops.append(op)
                l2s.append(l2)
            bodys.append(body)

        self.advance()  # ENDIF

        return If(l1s, ops, l2s, bodys)

    def if_const(self):
        body = []

        if self.tok.value == "else":
            self.advance()  # skip ELSE
            self.advance()  # skip ;

            while self.tok.value not in ("endif", "else", "elif"):
                body.append(self.expr())

            return None, None, None, body
        self.advance()  # skip IF,ELIF,ELSE,ENDIF
        l1 = Replace if self.tok.type == REPLACE else self.tok.value
        self.advance()
        op = Replace if self.tok.type == REPLACE else self.tok.value
        self.advance()
        l2 = Replace if self.tok.type == REPLACE else self.tok.value
        self.advance()

        self.advance()  # skip SEM

        while self.tok.value not in ("endif", "else", "elif"):
            body.append(self.expr())

        return l1, op, l2, body

    def match_return(self):
        returns = []

        while self.tok.type != SEM:
            if self.tok.type == REPLACE:
                returns.append(Replace)
            else:
                returns.append(self.tok.value)
            self.advance()

        self.advance()  # SKIP SEM

        return Return(returns)

    def match_call(self):
        name = self.tok.value
        args = []
        self.advance()

        while self.tok.type != SEM:
            if self.tok.type == REPLACE:
                args.append(Replace)
            else:
                args.append(self.tok.value)
            self.advance()
        self.advance()  # SEM
        return Call(name, args)

    def match_push(self):
        self.advance()  # skip Push

        val = self.tok.value
        self.advance()
        return Push(val)

    def match_while(self):
        self.advance()  # skip while
        expr1 = Replace if self.tok.type == REPLACE else self.tok.value

        self.advance()
        op = Replace if self.tok.type == REPLACE else self.tok.value

        self.advance()
        expr2 = Replace if self.tok.type == REPLACE else self.tok.value

        self.advance()  # skip expr2
        self.advance()  # skip :

        body = []
        while self.tok.value != "endwhile":
            body.append(self.expr())

        self.advance()  # endwhile

        return While(expr1, op, expr2, body)

    def match_get(self):
        self.advance()  # skip GET

        name = self.tok.value

        self.advance()  # skip Name

        return Get(name)

    def match_set(self):
        self.advance()  # skip SET

        name = self.tok.value
        self.advance()  # skip NAME
        value = Replace if self.tok.type == REPLACE else self.tok.value
        self.advance()  # skip VALUE

        return Set(name, value)

    def match_fn(self):
        args = []
        body = []

        self.advance()  # skip func

        if self.check_none():
            return

        name = self.tok.value

        self.advance()  # skip Name

        if self.check_none():
            return

        while self.tok and self.tok.type != COLON:
            args.append(self.tok.value)
            self.advance()

        self.advance()  # COLON

        while self.tok and self.tok.value != "endfunc":
            body.append(self.expr())

        self.advance()  # skip endfunc

        return Func(name, args, body)

    def match_command(self):
        self.advance()  # skip COMMAND

        name = self.tok.value
        body = []

        self.advance()  # skip Name

        self.advance()  # COLON

        while self.tok.value != "endcommand":
            body.append(self.expr())

        self.advance()  # skip endcommand

        return Command(name, body)

    def match_include(self):
        self.advance()

        path = self.tok.value

        self.advance()  # path
        self.advance()  # ;

        return Include(path)

    def catch_error(self):
        from .error import ObjError, NotCloseTag

        if not self.tok:
            hook._raise_error(NotCloseTag("", self.pos))

        elif self.tok.type == OBJ:
            hook._raise_error(ObjError(self.tok.value, self.pos))

    def check_none(self):
        if not self.tok:  # 保护
            self.catch_error()
            return True
