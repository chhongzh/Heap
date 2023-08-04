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


class Set:
    def __init__(self, name, val):
        self.name = name
        self.val = val


class Get:
    def __init__(self, name):
        self.name = name


class Add:
    pass


class Sub:
    pass


class Div:
    pass


class Mul:
    pass


class Print:
    pass


class Push:
    def __init__(self, val):
        self.val = val


class Replace:
    pass


class Pop:
    pass


class Input:
    def __init__(self, val: str):
        self.val = val


class Call:
    def __init__(self, name, args: list):
        self.name = name
        self.args = args


class Return:
    def __init__(self, vals: list):
        self.vals = vals


class Include:
    def __init__(self, path: str):
        self.path = path


class If:
    def __init__(self, l1s: list, ops: list, l2s: list, bodys: list) -> None:
        self.l1s = l1s
        self.ops = ops
        self.l2s = l2s
        self.bodys = bodys


class Command:
    def __init__(self, name: str, body: list):
        self.body = body
        self.name = name


class DotExpr:
    def __init__(self, father, child: list[str]):
        pass
