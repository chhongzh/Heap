from .stdlibs import LIBS
from .token import Token
from .asts import (
    Command,
    Div,
    Iter,
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
from .error import ERRDICT, SyntaxErr


class Builder:
    def __init__(self, toks: list[Token]):
        self.toks = toks
        self.pos = -1
        self.tok = None
        self.root = []

    def advance(self):
        """下一个token"""
        self.pos += 1
        if self.pos >= len(self.toks):
            self.tok = None
        else:
            self.tok = self.toks[self.pos]

    def eat(self, types: list):
        """检查类型并获得下一个token"""
        if not self.tok or self.tok.type not in types:
            hook._raise_error(
                SyntaxErr(
                    self.tok,
                    self.pos,
                    f"Need types:{repr(types)} , but get {self.tok.type if self.tok else 'None'}",
                )
            )

        self.advance()

    def parse(self):
        """构建Heap AST"""
        self.advance()
        while self.tok:
            self.root.append(self.expr())
        return Root(self.root)

    def expr(self):
        """解析一句表达式"""
        if self.tok.type == KEYWORD:
            match self.tok.value:
                case "func":
                    t = self.match_fn()

                    return t
                case "div":
                    self.advance()
                    self.eat([SEM])  # SEM

                    return Div()
                case "mul":
                    self.advance()
                    self.eat([SEM])  # SEM

                    return Mul()
                case "set":
                    t = self.match_set()
                    self.eat([SEM])  # SEM  # SEM

                    return t
                case "get":
                    t = self.match_get()
                    self.eat([SEM])  # SEM

                    return t
                case "push":
                    t = self.match_push()
                    self.eat([SEM])  # SEM  # SEM

                    return t
                case "print":
                    self.advance()  # PRINT
                    self.eat([SEM])  # SEM  # SEM

                    return Print()
                case "add":
                    self.advance()  # ADD
                    self.eat([SEM])  # SEM  # SEM

                    return Add()
                case "pop":
                    self.advance()  # pop
                    self.eat([SEM])  # SEM  # SEM

                    return Pop()
                case "sub":
                    self.advance()  # SUB
                    self.eat([SEM])  # SEM  # SEM

                    return Sub()
                case "return":
                    self.advance()  # RETURN
                    t = self.match_return()

                    return t
                case "while":
                    return self.match_while()
                case "if":
                    return self.match_if()
                case "include":
                    return self.match_include()
                case "command":
                    return self.match_command()
                case "input":
                    self.advance()  # Input
                    title = Replace if self.tok.type == REPLACE else self.tok.value
                    self.eat([OBJ])  # title
                    self.eat([SEM])  # SEM  # sem
                    return Input(title)

                case "iter":
                    return self.match_iter()
        elif self.tok.type == ID:
            return self.match_call()

        self.catch_error()  # 捕捉错误(无法识别的tok)
        self.advance()

    def match_if(self):
        """捕捉IF语句"""

        l1s = []  # 条件
        ops = []  # 符号
        l2s = []  # 条件
        bodys = []  # 块语句

        while self.tok.value != "endif":
            l1, op, l2, body = self.if_const()
            if None not in (l1, op, l2):
                l1s.append(l1)
                ops.append(op)
                l2s.append(l2)
            bodys.append(body)

        self.eat([KEYWORD])  # ENDIF

        return If(l1s, ops, l2s, bodys)

    def if_const(self):
        body = []

        if self.tok.value == "else":
            self.advance()  # skip ELSE
            self.eat([COLON])  # skip ;

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

        self.eat([COLON])  # skip SEM

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
        self.eat([SEM])  # SEM
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
        self.eat([COLON])  # skip :

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

        name = self.tok.value

        self.advance()  # skip Name

        while self.tok and self.tok.type != COLON:
            args.append(self.tok.value)
            self.advance()

        self.eat([COLON])  # COLON

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
        self.eat([SEM])  # ;

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

    def match_iter(self):
        self.advance()  # skip keyword

        iter_item = Replace if self.tok.type == REPLACE else self.tok.value
        body = []

        self.advance()  # skip list

        iter_name = self.tok.value
        self.advance()

        self.eat([COLON])  # skip :

        while not self.current_is_keyword("enditer"):
            body.append(self.expr())

        self.advance()  # Skip enditer
        return Iter(iter_item, iter_name, body)

    def current_is_keyword(self, keyword: str):
        return self.tok.type == KEYWORD and self.tok.value == keyword
