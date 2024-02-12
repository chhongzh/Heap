from .ast import (
    BinExpr,
    BoolExpr,
    Break,
    Call,
    Func,
    If,
    Var,
    VarDecl,
    Return,
    VarSet,
    While,
    Continue,
)


class Analyzer:
    def __init__(self, toks: list) -> None:
        self._toks = toks
        self._pos = -1
        self._current = None

    def parse(self):
        return self.parse_lot(self._toks)

    def parse_lot(self, toks: list):
        statements = []
        for statement in toks:
            statements.append(self.parse_statement(statement))

        return statements

    def parse_statement(self, statement):
        if statement[0] == "var":
            if len(statement) >= 5:  # With default value
                return VarDecl(
                    statement[2], statement[1], self.parse_expr(statement[4])
                )
            elif len(statement) == 3:
                return VarDecl(statement[2], statement[1])
        elif len(statement) == 3 and statement[1] == "=":
            return VarSet(statement[0], self.parse_expr(statement[2]))
        elif len(statement) == 1 and statement[0] == "continue":
            return Continue()
        elif len(statement) == 1 and statement[0] == "break":
            return Break()
        elif statement[0] == "while":
            return While(self.parse_lot(statement[2]), self.parse_expr(statement[1]))
        elif statement[0] == "func":
            ret_type = statement[1]
            name = statement[2]

            TB = {}
            i = 0
            while i < len(statement[3]):  # 匹配TB
                TB[statement[3][i + 1]] = statement[3][i]
                i += 2
            body = self.parse_lot(statement[4])
            return Func(ret_type, name, TB, body)
        elif statement[0] == "return":
            return Return(self.parse_expr(statement[1]))
        elif statement[0] == "if":
            idx = 0
            conditions = []
            body = []
            while idx < len(statement):

                type = statement[idx]
                if type in ("if", "elif"):
                    conditions.append(self.parse_expr(statement[idx + 1]))
                    body.append(self.parse_lot(statement[idx + 2]))
                else:
                    body.append(self.parse_lot(statement[idx + 1]))

                idx += 3

            return If(body, conditions)
        else:

            return self.parse_expr(statement)

    def parse_expr(self, expr):
        return self.parse_bool_expr(expr)

    def parse_bool_expr(self, bool_expr: list):
        if len(bool_expr) == 1:  # 只有一项, 不需要求值
            return self.parse_bin_expr(bool_expr[0])
        else:
            left = self.parse_bin_expr(bool_expr[0])
            op = bool_expr[1]
            right = self.parse_bin_expr(bool_expr[2])
            return BoolExpr(left, op, right)

    def parse_bin_expr(self, bin_expr: list):
        if not isinstance(bin_expr, list):  # 直接对象
            if bin_expr == "false":
                return False
            if bin_expr == "true":
                return True
            if isinstance(bin_expr, str):
                return Var(bin_expr)
            return bin_expr
        if len(bin_expr) == 1:  # 只有一项, 直接返回实值
            return self.parse_bin_expr(bin_expr[0])
        elif len(bin_expr) == 2:
            return self.parse_call(bin_expr)
        elif len(bin_expr) == 3 and bin_expr[0] == '"' and bin_expr[2] == '"':
            return bin_expr[1]

        idx = 3
        left = self.parse_bin_expr(bin_expr[0])
        op = bin_expr[1]
        right = self.parse_bin_expr(bin_expr[2])

        big_left = BinExpr(left, op, right)

        while idx < len(bin_expr):
            idx += 2

            big_left = BinExpr(
                big_left, bin_expr[idx - 2], self.parse_bin_expr(bin_expr[idx - 1])
            )

        return big_left

    def parse_call(self, expr: list):
        name, args = expr

        return Call(name, [self.parse_bool_expr(arg) for arg in args])
