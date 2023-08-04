"""
Heap Lang!
"""


from time import time

from .. import Lexer, Builder
from ..asts import (
    Call,
    Get,
    Include,
    Print,
    Push,
    Replace,
    Root,
    Func,
    Add,
    Sub,
    Mul,
    Div,
    Set,
    Input,
)

from ..loader import loader


class Compiler:
    def __init__(
        self,
        code: Root,
        method_prefix="",
        builtin_method_prefix="_heap_func__",
        line_end_prefix="\n",
        fn_var_prefix="heap__",
        user_var_prefix="heap_user_var__",
        user_func_prefix="heap_user_func__",
    ):
        self.method_prefix = method_prefix
        self.builtin_method_prefix = builtin_method_prefix
        self.line_end_prefix = line_end_prefix
        self.fn_var_prefix = fn_var_prefix
        self.user_var_prefix = user_var_prefix
        self.user_func_prefix = user_func_prefix

        self.indent = 0

        self.code = code
        # 这是Heap语言的指令
        self.body = [
            # Builtin Vars:
            f"{builtin_method_prefix}STACK = []{line_end_prefix}",
            # Builtin Method:
            # Push
            f"def {builtin_method_prefix}push({fn_var_prefix}stk,{fn_var_prefix}val):{line_end_prefix}",
            f"    {fn_var_prefix}stk.append({fn_var_prefix}val){line_end_prefix}",
            # Print
            f"def {builtin_method_prefix}print({fn_var_prefix}stk):{line_end_prefix}",
            f"    print({fn_var_prefix}stk.pop(),end=''){line_end_prefix}",
            # Input
            f"def {builtin_method_prefix}input({fn_var_prefix}stk,{fn_var_prefix}var):{line_end_prefix}",
            f"    {fn_var_prefix}stk.append(input({fn_var_prefix}var)){line_end_prefix}",
            # Add
            f"def {builtin_method_prefix}add({fn_var_prefix}stk):{line_end_prefix}",
            f"    {fn_var_prefix}b={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}a={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}stk.append({fn_var_prefix}a+{fn_var_prefix}b){line_end_prefix}",
            # Sub
            f"def {builtin_method_prefix}sub({fn_var_prefix}stk):{line_end_prefix}",
            f"    {fn_var_prefix}b={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}a={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}stk.append({fn_var_prefix}a-{fn_var_prefix}b){line_end_prefix}",
            # Div
            f"def {builtin_method_prefix}div({fn_var_prefix}stk):{line_end_prefix}",
            f"    {fn_var_prefix}b={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}a={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}stk.append({fn_var_prefix}a/{fn_var_prefix}b){line_end_prefix}",
            # Mul
            f"def {builtin_method_prefix}mul({fn_var_prefix}stk):{line_end_prefix}",
            f"    {fn_var_prefix}b={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}a={fn_var_prefix}stk.pop(){line_end_prefix}",
            f"    {fn_var_prefix}stk.append({fn_var_prefix}a*{fn_var_prefix}b){line_end_prefix}",
        ]

        self.insert_header()

    def insert_header(self):
        self.body.insert(
            0,
            f"# This file is compile by Heap Lang Compiler.{self.line_end_prefix}",
        )
        self.body.insert(
            1,
            f"# Changing this file has no effect on the source file.{self.line_end_prefix}",
        )
        self.body.insert(
            2,
            f"# Compile at {time()}.{self.line_end_prefix}",
        )

    def append_comment(self, comment: str):
        self.body.append(f"{self.get_space()}# {comment}{self.line_end_prefix}")

    def include(self, path):
        l = Lexer(loader(path))
        tok = l.lex()
        b = Builder(tok)
        asts = b.parase()

        self.append_comment(f"Include File {path}")
        self.compile_lot(asts.body)
        self.append_comment(f"End Include File {path}")

    def compile(self):
        self.append_statement("")
        self.append_comment("BEGAIN TO MAIN!")

        self.compile_lot(self.code.body)

        self.append_comment("END MAIN!")
        self.append_statement("")

        print("Compile Done! Errors:0 Warnings:0 Info:0")
        return self.body

    def get_space(self):
        return "    " * self.indent

    def make_replace_to(self, lst: list):
        replace_count = lst.count(Replace)
        args = []

        for idx in range(len(lst)):
            if lst[idx] == Replace:
                args.append(f"{self.builtin_method_prefix}STACK[-{replace_count}]")
                replace_count -= 1
            else:
                args.append(self.obj_to_pyobj(lst[idx]))

        return args

    def make_del(self, count):
        return f"del {self.builtin_method_prefix}STACK[-{count}:]"

    def obj_to_pyobj(self, obj):
        if isinstance(obj, str):
            return f"'{obj}'"
        return f"{obj}"

    def append_statements(self, list: list):
        temp1 = "\n"
        temp2 = "\\n"
        self.body.extend(
            [
                f"{self.get_space()}{i.replace(temp1,temp2)}{self.line_end_prefix}"
                for i in list
            ]
        )

    def append_statement(self, raw_string: str):
        temp1 = "\n"
        temp2 = "\\n"
        self.body.append(
            f"{self.get_space()}{raw_string.replace(temp1,temp2)}{self.line_end_prefix}"
        )

    def call_builtin(self, name, args: list):
        self.append_statement(
            f"{self.builtin_method_prefix}{name}({self.builtin_method_prefix}STACK{',' if args else ''}{','.join(args)})"
        )

    def compile_lot(self, lst: list):
        for item in lst:
            self.compile_one(item)

    def append_func(self, name: str, args: list[str], body: list):
        self.append_statement(f'def {self.user_func_prefix}{name}({",".join(args)}):')
        self.indent += 1
        self.append_statement(f"{self.builtin_method_prefix}STACK = []")
        self.compile_lot(body)
        self.indent -= 1

    def compile_one(self, node):
        if isinstance(node, Func):
            self.append_func(
                node.name, [f"{self.user_var_prefix}{i}" for i in node.args], node.body
            )
        elif isinstance(node, Push):
            self.call_builtin("push", self.make_replace_to([node.val]))
        elif isinstance(node, Print):
            self.call_builtin("print", [])
        elif isinstance(node, Add):
            self.call_builtin("add", [])
        elif isinstance(node, Sub):
            self.call_builtin("sub", [])
        elif isinstance(node, Div):
            self.call_builtin("div", [])
        elif isinstance(node, Mul):
            self.call_builtin("mul", [])
        elif isinstance(node, Input):
            self.call_builtin("input", self.make_replace_to([node.val]))
        elif isinstance(node, Set):
            val = self.make_replace_to([node.val])[0]

            self.append_statements(
                [
                    f"{self.user_var_prefix}{node.name} = {val}",
                    self.make_del(1),
                ]
            )
        elif isinstance(node, Get):
            self.append_statement(
                f"{self.builtin_method_prefix}STACK.append({self.user_var_prefix}{node.name})"
            )
        elif isinstance(node, Call):
            args = self.make_replace_to(node.args)
            self.append_statement(
                f"{self.user_func_prefix}{node.name}({','.join(args)})"
            )
            self.append_statement(self.make_del(len(args)))
        elif isinstance(node, Include):
            self.include(node.path)
