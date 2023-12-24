# Heap @ 2023
# chhongzh

"""
Heap的所有ast节点
"""

from typing import Any
import abc
from .token import Token


class Node(abc.ABC):
    def __repr__(self) -> str:
        "返回字符串格式, 这个方法必须重载"


class Root(Node):
    def __init__(self, body: list = None, file_path=None):
        self.body = body
        self.var_ctx = {}
        self.stack = []
        self.command = {}
        self.runner: Any
        self.file_path = file_path

        self.var_ctx: dict[str, Func]

    def append(self, tok: Token):
        """增加一个节点"""

        self.body: list
        self.body.append(tok)

    def __repr__(self):
        return f"Root({repr(self.body)})"


class Try(Node):
    def __init__(self, t1: list, catch: list, t2: list):
        pass


class Func(Node):
    def __init__(self, name: str, args: list[str], body: list = None):
        self.args = args
        self.name = name
        self.body = body
        self.var_ctx = {}
        self.stack = []
        self.command = {}

    def append(self, tok: Token):
        """添加一个节点"""
        self.body.append(tok)

    def __repr__(self):
        return f"Func({repr(self.name)},{repr(self.args)},{repr(self.body)})"


class Set(Node):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __repr__(self):
        return f"Set({repr(self.name)},{repr(self.val)})"


class Get(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Get({repr(self.name)})"


class Add(Node):
    def __repr__(self):
        return "Add()"


class Sub(Node):
    def __repr__(self):
        return "Sub()"


class Div(Node):
    def __repr__(self):
        return "Div()"


class Mul(Node):
    def __repr__(self):
        return "Mul()"


class Print(Node):
    def __repr__(self):
        return "Print()"


class Push(Node):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"Push({repr(self.val)})"


class Replace(Node):
    def __repr__(self):
        return "Replace()"


class Pop(Node):
    def __repr__(self):
        return "Pop()"


class Input(Node):
    def __init__(self, val: str):
        self.val = val

    def __repr__(self):
        return f"Input({repr(self.val)})"


class Call(Node):
    def __init__(self, name, args: list):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Call({repr(self.name)},{repr(self.args)})"


class Return(Node):
    def __init__(self, vals: list):
        self.vals = vals

    def __repr__(self):
        return f"Return({repr(self.vals)})"


class Include(Node):
    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f"Include({repr(self.path)})"


class If(Node):
    def __init__(self, l1s: list, ops: list, l2s: list, bodys: list) -> None:
        self.l1s = l1s
        self.ops = ops
        self.l2s = l2s
        self.bodys = bodys

    def __repr__(self):
        return (
            f"If({repr(self.l1s)},{repr(self.ops)},{repr(self.l2s)},{repr(self.bodys)})"
        )


class Command(Node):
    def __init__(self, name: str, body: list):
        self.body = body
        self.name = name

    def __repr__(self):
        return f"Command({repr(self.name)},{repr(self.body)})"


class DotExpr(Node):
    def __init__(self, father, child: list[str]):
        pass

    def __repr__(self) -> str:
        return "You Can't do this."


class While(Node):
    def __init__(self, expr1, op, expr2, body: list):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2
        self.body = body

    def __repr__(self):
        return f"While({repr(self.expr1)},{repr(self.op)},{repr(self.expr2)},{repr(self.body)})"


class Iter(Node):
    def __init__(self, val, iter_name, body: list):
        self.val = val
        self.iter_name = iter_name
        self.body = body

    def __repr__(self):
        return f"Iter({repr(self.val)},{repr(self.iter_name)},{repr(self.body)})"


class LinkExpr(Node):
    def __init__(self, value, call_chain: list, arg_chain: list) -> None:
        self.value = value
        self.call_chain = call_chain
        self.arg_chain = arg_chain

    def __repr__(self):
        return f"LinkExpr({repr(self.value)},{repr(self.call_chain)},{repr(self.arg_chain)})"
