from .common import Evalable
from .libpy import _builtin
from .libpy import _math
from .libpy import _cast
from .bind import bind_from_module


class Runner:
    def __init__(self, toks: list, bind: bool = True):
        self.toks = toks
        self.context = {"object": {}, "typebound": {}}

        if bind:
            bind_from_module(self.context, _builtin)
            bind_from_module(self.context, _cast)
            bind_from_module(self.context, _math)

    def run(self):
        return self._run_lot(self.toks, self.context)

    def _run(self, statement: Evalable, ctx: dict):
        return statement.eval(self, ctx)

    def _run_lot(self, statements: list, ctx: dict):
        l_val = None
        l_type = None
        for statement in statements:
            val, type, ret, brk = self._run(statement, ctx)
            if val != None:

                l_val = val
                l_type = type
        return l_val, l_type, False, 0
