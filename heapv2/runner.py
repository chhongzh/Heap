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
        self._run_lot(self.toks, self.context)

    def _run(self, statement: Evalable, ctx: dict):
        statement.eval(self, ctx)

    def _run_lot(self, statements: list, ctx: dict):
        for statement in statements:
            self._run(statement, ctx)
