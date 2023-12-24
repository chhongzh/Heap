# Heap @ 2023
# chhongzh

"""构建Heap AST树的模块"""

from .token import Token
from .asts import (
    Command,
    Div,
    Iter,
    LinkExpr,
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
    While,
)
from .types import EQUAL, LINK, OBJ, SEM, KEYWORD, REPLACE, ID, COLON
from . import hook
from .error import NotCloseTag, ObjError, SyntaxErr
from .log import info


class Builder:
    def __init__(self, toks: list[Token], file_path=None):
        self.toks = toks
        self.pos = -1
        self.tok = None
        self.root = []
        self.will_raise_next = None
        self.file_path = file_path

        info("[Builder]: 就绪")

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
            hook.raise_error(
                SyntaxErr(
                    self.tok,
                    self.pos,
                    f"Need types:{repr(types)} , but get {self.tok.type if self.tok else 'None'}",
                )
            )

        self.advance()

    def parse(self):
        """构建Heap AST"""
        info("[Builder]: 开始构建")
        self.advance()
        while self.tok:
            self.root.append(self.expr())
        info("[Builder]: 构建结束")
        return Root(self.root, self.file_path)

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

                case _:
                    hook.print_error(SyntaxErr(self.tok.value, self.pos, "未知的符号"))

                    return None
        elif self.tok.type == ID:
            has_next_tok = (len(self.toks) - self.pos) > 1
            if has_next_tok:
                next_tok = self.toks[self.pos + 1]
                next_tok: Token
                if next_tok.type == EQUAL:
                    return self.match_assignment()
            return self.match_call()

        elif self.tok.type in (OBJ, REPLACE) and self.toks[self.pos + 1].type == LINK:
            return self.match_link()

        self.catch_error()  # 捕捉错误(无法识别的tok)
        self.advance()

        return None

    def match_assignment(self):
        name = self.tok.value
        self.eat([ID])

        self.eat([EQUAL])

        value = self.tok.value if self.tok.type != REPLACE else Replace

        self.eat([OBJ, REPLACE])

        self.eat([SEM])

        return Set(name, value)

    def match_link(self):
        """捕捉Match Link"""

        value = self.tok.value if self.tok.type != REPLACE else Replace
        call_chain = []
        arg_chain = []

        self.eat([OBJ, REPLACE])

        while self.tok.type != SEM:
            arg = []
            self.eat([LINK])

            call_chain.append(self.tok.value)
            self.eat([ID])

            while self.tok.type not in (SEM, LINK):
                if self.tok.type == REPLACE:
                    arg.append(Replace)
                else:
                    arg.append(self.tok.value)

                self.eat([REPLACE, OBJ])

            arg_chain.append(arg)

        self.eat([SEM])

        return LinkExpr(value, call_chain, arg_chain)

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
        "匹配if结构"

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
        "匹配return语句"

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
        "匹配调用语句"

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
        "匹配push语句"

        self.advance()  # skip Push

        val = self.tok.value
        self.advance()
        return Push(val)

    def match_while(self):
        "匹配while语句"

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
        "匹配get语句"

        self.advance()  # skip GET

        name = self.tok.value

        self.advance()  # skip Name

        return Get(name)

    def match_set(self):
        "匹配set语句"

        self.advance()  # skip SET

        name = self.tok.value
        self.advance()  # skip NAME
        value = Replace if self.tok.type == REPLACE else self.tok.value
        self.advance()  # skip VALUE

        return Set(name, value)

    def match_fn(self):
        "匹配函数定义"

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
        "匹配命令定义"

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
        "匹配include语句"

        self.advance()

        path = self.tok.value

        self.advance()  # path
        self.eat([SEM])  # ;

        return Include(path)

    def catch_error(self):
        "生成并捕捉错误"

        if not self.tok:
            hook.raise_error(NotCloseTag("", self.pos))

        elif self.tok.type == OBJ:
            hook.raise_error(
                ObjError(self.tok.value, self.pos, "OBJ不能单独作为一行, 除非Link表达式")
            )

    def check_none(self):
        """检查是否是None"""

        if not self.tok:  # 保护
            self.catch_error()
            return True
        return False

    def match_iter(self):
        "匹配iter"

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
        "判断当前是否是关键字"

        return self.tok.value == keyword and self.tok.type == KEYWORD
