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
    Variable,
    Try,
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
        self.has_next_tok = None

        info("[Builder]: 就绪")

    def advance(self):
        """下一个token"""
        self.pos += 1
        if self.pos >= len(self.toks):
            self.tok = None
            self.has_next_tok = False
        else:
            if self.pos >= len(self.toks) - 1:
                self.has_next_tok = False
            else:
                self.has_next_tok = True
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
            if self.tok.value == "func":
                t = self.match_fn()

                return t
            elif self.tok.value == "div":
                meta_info = self.tok.meta
                self.advance()
                self.eat([SEM])  # SEM
                temp = Div()
                temp.meta_info = meta_info

                return
            elif self.tok.value == "mul":
                self.advance()
                meta_info = self.tok.meta
                self.eat([SEM])  # SEM

                temp = Mul()
                temp.meta_info = meta_info

                return temp
            elif self.tok.value == "set":
                meta_info = self.tok.meta

                t = self.match_set()
                self.eat([SEM])  # SEM  # SEM

                t.meta_info = meta_info

                return t
            elif self.tok.value == "get":
                meta_info = self.tok.meta

                t = self.match_get()
                self.eat([SEM])  # SEM

                t.meta_info = meta_info
                return t
            elif self.tok.value == "push":
                meta_info = self.tok.meta

                t = self.match_push()
                self.eat([SEM])  # SEM  # SEM

                t.meta_info = meta_info

                return t
            elif self.tok.value == "print":
                self.advance()  # PRINT
                meta_info = self.tok.meta

                self.eat([SEM])  # SEM  # SEM

                temp = Print()
                temp.meta_info = meta_info

                return Print()
            elif self.tok.value == "add":
                self.advance()  # ADD
                meta_info = self.tok.meta
                self.eat([SEM])  # SEM  # SEM

                t = Add()
                t.meta_info = meta_info

                return t
            elif self.tok.value == "pop":
                self.advance()  # pop
                meta_info = self.tok.meta
                self.eat([SEM])  # SEM  # SEM

                t = Pop()
                t.meta_info = meta_info
                return t
            elif self.tok.value == "sub":
                self.advance()  # SUB
                meta_info = self.tok.meta
                self.eat([SEM])  # SEM  # SEM

                t = Sub()
                t.meta_info = meta_info
                return t
            elif self.tok.value == "return":
                meta_info = self.tok.meta
                self.advance()  # RETURN
                t = self.match_return()

                t.meta_info = meta_info

                return t
            elif self.tok.value == "while":
                meta_info = self.tok.meta
                t = self.match_while()
                t.meta_info = meta_info
                return t
            elif self.tok.value == "if":
                meta_info = self.tok.meta

                t = self.match_if()
                t.meta_info = meta_info

                return t
            elif self.tok.value == "include":
                meta_info = self.tok.meta

                t = self.match_include()
                t.meta_info = meta_info

                return t
            elif self.tok.value == "command":
                meta_info = self.tok.meta

                t = self.match_command()
                t.meta_info = meta_info

                return t
            elif self.tok.value == "input":
                meta_info = self.tok.meta
                self.advance()  # Input

                title = (
                    self.variable_or_replace()
                    if self.tok.type in (ID, REPLACE)
                    else self.tok.value
                )

                self.eat([OBJ])  # title
                self.eat([SEM])  # SEM  # sem
                t = Input(title)
                t.meta_info = meta_info
                return t

            elif self.tok.value == "iter":
                meta_info = self.tok.meta
                t = self.match_iter()
                t.meta_info = meta_info

                return t

            elif self.tok.value == "try":
                t = self.match_try()

                return t

            else:
                hook.print_error(SyntaxErr(self.tok.value, self.pos, "未知的符号"))

                return None

        elif (
            self.tok.type in (OBJ, REPLACE, ID)
            and self.has_next_tok
            and self.toks[self.pos + 1].type == LINK
        ):
            meta_info = self.tok.meta
            t = self.match_link()
            t.meta_info = meta_info
            return t

        elif (
            self.tok.type == ID
            and self.has_next_tok
            and self.toks[self.pos + 1].type == EQUAL
        ):
            meta_info = self.tok.meta

            t = self.match_assignment()
            t.meta_info = meta_info

            return t
        elif self.tok.type == ID:
            meta_info = self.tok.meta

            t = self.match_call()
            t.meta_info = meta_info

            return t

        self.catch_error()  # 捕捉错误(无法识别的tok)
        self.advance()

        return None

    def match_try(self):
        meta_info = self.tok.meta

        try_block = []
        catches = []
        blocks = []

        self.eat([KEYWORD])
        self.eat([COLON])

        while self.tok.value not in ("catch"):
            try_block.append(self.expr())

        while self.tok.value != "endtry":
            catch, body = self.try_const()

            blocks.append(body)
            catches.append(catch)

        self.eat([KEYWORD])  # ENDIF

        return Try(try_block, catches, blocks)

    def try_const(self):
        self.advance()  # skip try

        catches = []
        body = []

        while self.tok.type != COLON:
            catches.append(self.tok.value)
            self.eat([ID])

        self.eat([COLON])

        while self.tok.value not in ("endtry", "catch"):
            body.append(self.expr())

        return catches, body

    def match_assignment(self):
        name = self.tok.value
        self.eat([ID])

        self.eat([EQUAL])

        value = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )

        self.eat([OBJ, REPLACE, ID])

        self.eat([SEM])

        return Set(name, value)

    def match_link(self):
        """捕捉Match Link"""

        value = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )
        call_chain = []
        arg_chain = []

        self.eat([OBJ, REPLACE, ID])

        while self.tok.type != SEM:
            arg = []
            self.eat([LINK])

            call_chain.append(self.tok.value)
            self.eat([ID])

            while self.tok.type not in (SEM, LINK):
                arg.append(
                    self.variable_or_replace()
                    if self.tok.type in (ID, REPLACE)
                    else self.tok.value
                )

                self.eat([REPLACE, OBJ, ID])

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

    def variable_or_replace(self):
        if self.tok.type == REPLACE:
            return Replace

        elif self.tok.type == ID:
            return Variable(self.tok.value)

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
        l1 = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )
        self.advance()
        op = self.tok.value
        self.advance()
        l2 = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )
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
            elif self.tok.type == ID:
                returns.append(Variable(self.tok.value))
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

        while self.tok is not None and self.tok.type != SEM:
            if self.tok.type == REPLACE:
                args.append(Replace)
            elif self.tok.type == ID:
                args.append(Variable(self.tok.value))
            else:
                args.append(self.tok.value)
            self.advance()

        if self.tok is None:
            hook.raise_error(
                SyntaxErr(
                    None,
                    -1,
                    f'在行{self.toks[self.pos - 1].meta.line_no}. 一处调用从未被关闭. (缺少";"?)',
                )
            )
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
        expr1 = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )

        self.advance()
        op = self.tok.value

        self.advance()
        expr2 = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )

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
        value = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )
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

        iter_item = (
            self.variable_or_replace()
            if self.tok.type in (ID, REPLACE)
            else self.tok.value
        )
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
