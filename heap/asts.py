from .token import Token


class Root:
    def __init__(self, body=[]):
        self.body = body
        self.var_ctx = {}
        self.fn_ctx = {}
        self.stack = []
        self.command = {}

        self.fn_ctx: dict[str, Func]

    def append(self, tok: Token):
        self.body: list
        self.body.append(tok)

    def __repr__(self):
        return f"Root({self.body.__repr__()})"


class Try:
    def __init__(self, t1: list, catch: list, t2: list):
        pass


class Func:
    def __init__(self, name: str, args: list[str], body=[]):
        self.args = args
        self.name = name
        self.body = body
        self.var_ctx = {}
        self.fn_ctx = {}
        self.stack = []
        self.command = {}

        self.fn_ctx: dict[str, Func]

    def append(self, tok: Token):
        self.body: list
        self.body.append(tok)

    def __repr__(self):
        return f"Func({self.name.__repr__()},{self.args.__repr__()},{self.body.__repr__()})"


class Set:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def __repr__(self):
        return f"Set({self.name.__repr__()},{self.val.__repr__()})"


class Get:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Get({self.name.__repr__()})"


class Add:
    def __repr__(self):
        return f"Add()"


class Sub:
    def __repr__(self):
        return f"Sub()"


class Div:
    def __repr__(self):
        return f"Div()"


class Mul:
    def __repr__(self):
        return f"Mul()"


class Print:
    def __repr__(self):
        return f"Print()"


class Push:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"Push({self.val.__repr__()})"


class Replace:
    def __repr__(self):
        return f"Replace()"


class Pop:
    def __repr__(self):
        return f"Pop()"


class Input:
    def __init__(self, val: str):
        self.val = val

    def __repr__(self):
        return f"Input({self.val.__repr__()})"


class Call:
    def __init__(self, name, args: list):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Call({self.name.__repr__()},{self.args.__repr__()})"


class Return:
    def __init__(self, vals: list):
        self.vals = vals

    def __repr__(self):
        return f"Return({self.vals.__repr__()})"


class Include:
    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f"Include({self.path.__repr__()})"


class If:
    def __init__(self, l1s: list, ops: list, l2s: list, bodys: list) -> None:
        self.l1s = l1s
        self.ops = ops
        self.l2s = l2s
        self.bodys = bodys

    def __repr__(self):
        return f"If({self.l1s.__repr__()},{self.ops.__repr__()},{self.l2s.__repr__()},{self.bodys.__repr__()})"


class Command:
    def __init__(self, name: str, body: list):
        self.body = body
        self.name = name

    def __repr__(self):
        return f"Command({self.name.__repr__()},{self.body.__repr__()})"


class DotExpr:
    def __init__(self, father, child: list[str]):
        pass


class While:
    def __init__(self, expr1, op, expr2, body: list):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2
        self.body = body

    def __repr__(self):
        return f"While({self.expr1.__repr__()},{self.op.__repr__()},{self.expr2.__repr__()},{self.body.__repr__()})"
