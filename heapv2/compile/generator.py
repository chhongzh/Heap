from ..ast import ASTNode, Func, BinExpr, Return


class Generator:
    def __init__(self, ast: list[ASTNode]):
        self._ast = ast
        self._line = []

        self._typename = {"int": "i64"}
        self._tab_cnt = 0

    def generate(self):
        self._lot(self._ast, {"register": 1})
        for line in self._line:
            print(line)

    def _one(self, t: Func | BinExpr, cfg: dict):
        if isinstance(t, Func):
            self._log("Translate Func")

            fn_name = t.name
            fn_type = self._typename[t.type]
            fn_arg = []

            self._log(f"Func name: {fn_name}")
            self._log(f"Func type: {t.type}, so LLVM ir type: {fn_type}")
            self._log(f"Arg count: {len(t.tb)}")

            for name, type in t.tb.items():
                arg = f"{self._typename[type]} %{name}"
                fn_arg.append(f"{arg}")
                self._log(f"Func arg: {arg}")

            fn_head = f"define {fn_type} @{fn_name}({', '.join(fn_arg)}){{"
            self._log(f"Head is {fn_head}")

            # 翻译下面
            self._add_line(fn_head)
            self._lot(t.body, {"register": 1, "func_ret": fn_type})
            self._add_line("}")

        elif isinstance(t, (Return)):
            self._add_line(f"ret {cfg['func_ret']} ")

    def _lot(self, lst: list[ASTNode], cfg: dict):
        for l in lst:
            self._one(l, cfg)

    def _log(self, message: str):
        print(f"Compiler: {message}")

    def _add_line(self, line):
        self._line.append(f'{" "*self._tab_cnt}{line}')
