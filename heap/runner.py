from os import getcwd
from .error import *
from .asts import (
    Div,
    Input,
    Mul,
    Pop,
    Root,
    Func,
    Set,
    Get,
    Push,
    Print,
    Call,
    Replace,
    Return,
    Sub,
    Add,
    If,
    Include,
    Command,
)
from os.path import exists, dirname, join
from inspect import isfunction
from . import hook
from .loader import loader
from . import Lexer, Builder
from .stdlibs import LIBS
from importlib import import_module


class Runner:
    def __init__(self, root: Root, path: str):
        self.root = root
        self.include_path = [path]

    def run(self):
        self.visits(self.root.body, self.root)

    def visit(self, node, father: Root | Func):
        if isinstance(node, Func):
            father.fn_ctx[node.name] = node
        elif isinstance(node, Input):
            father.stack.append(input(self.expr_args([node.val], father)[0]))
        elif isinstance(node, Command):
            father.command[node.name] = node
        elif isinstance(node, Set):
            father.var_ctx[node.name] = self.expr_args([node.val], father)[0]
        elif isinstance(node, Get):
            father.stack.append(father.var_ctx[node.name])
        elif isinstance(node, Push):
            father.stack.append(node.val)
        elif isinstance(node, Pop):
            self.try_pop(father)
        elif isinstance(node, Print):
            hook._print(self.try_pop(father))
        elif isinstance(node, Call):
            self.call(node, father)
        elif isinstance(node, Return):
            return self.expr_args(node.vals, father)
        elif isinstance(node, Sub):
            b, a = self.try_pop(father), self.try_pop(father)
            father.stack.append(a - b)
        elif isinstance(node, Add):
            b, a = self.try_pop(father), self.try_pop(father)
            father.stack.append(a + b)
        elif isinstance(node, Mul):
            b, a = self.try_pop(father), self.try_pop(father)
            father.stack.append(a * b)
        elif isinstance(node, Div):
            b, a = self.try_pop(father), self.try_pop(father)
            father.stack.append(a / b)
        elif isinstance(node, If):
            self.expr_if(node, father)
        elif isinstance(node, Include):
            self.load_module(node.path, father)

    def load_module(self, path: str, father: Func | Root):
        if path in LIBS:
            md = import_module(f".lib.{LIBS[path]}", "heap")
            for name in md.__dir__():
                if (
                    not name.startswith("__")
                    and not name.endswith("__")
                    and isfunction(md.__dict__[name])
                ):
                    father.fn_ctx[name] = md.__dict__[name]
            return

        path = join(self.include_path[-1], path)
        self.include_path.append(dirname(path))

        if not exists(path):
            hook._raise_error(IncludeError(path, -1, "Not a file."))
            return

        content = loader(path)
        lexer = Lexer(content)
        toks = lexer.lex()

        builder = Builder(toks)
        ast = builder.parase()
        self.visits(ast.body, father)

        self.include_path.pop()

    def expr_args(self, args: list, father: Func | Root, delete=True):
        replace_count = args.count(Replace)
        replace_args = father.stack[len(father.stack) - replace_count :]
        idx = 0
        args_list = []
        for arg in args:
            if arg == Replace:
                args_list.append(replace_args[idx])
                idx += 1
            else:
                args_list.append(arg)

        if delete:
            del father.stack[len(father.stack) - replace_count :]  # 删除内容

        return args_list

    def expr_if(self, node: If, father: Root | Func):
        if not (len(node.l1s) == len(node.l2s) == len(node.ops)):
            raise Exception

        else:
            # if-else mode:
            if len(node.l1s) + 1 == len(node.bodys):
                for l1, op, l2, body in zip(
                    node.l1s, node.ops, node.l2s, node.bodys[:-1]
                ):
                    l1, op, l2 = self.expr_args([l1, op, l2], father, False)

                    if op == "EQUAL" and l1 == l2:
                        self.visits(body, father)
                        break
                    elif op == "BIGEQUAL" and l1 >= l2:
                        self.visits(body, father)
                        break
                    elif op == "SMALLER" and l1 < l2:
                        self.visits(body, father)
                        break
                    elif op == "SMALLEQUAL" and l1 <= l2:
                        self.visits(body, father)
                        break
                    elif op == "NOTEQUAL" and l1 != l2:
                        self.visits(body, father)
                        break
                else:
                    self.visits(node.bodys[-1], father)

            elif len(node.l1s) == len(node.bodys):
                for l1, op, l2, body in zip(node.l1s, node.ops, node.l2s, node.bodys):
                    l1, op, l2 = self.expr_args([l1, op, l2], father, False)

                    if op == "EQUAL" and l1 == l2:
                        self.visits(body, father)
                        break
                    elif op == "BIGEQUAL" and l1 >= l2:
                        self.visits(body, father)
                        break
                    elif op == "SMALLER" and l1 < l2:
                        self.visits(body, father)
                        break
                    elif op == "SMALLEQUAL" and l1 <= l2:
                        self.visits(body, father)
                        break
                    elif op == "NOTEQUAL" and l1 != l2:
                        self.visits(body, father)
                        break
                else:
                    self.visits(node.bodys[-1], father)
            else:
                raise Exception(len(node.l1s), len(node.bodys))

    def call(self, node: Call, father: Root | Func):
        if node.name in father.command:
            if node.args:
                raise Exception

            self.visits(father.command[node.name].body, father)
            return

        args_list = self.expr_args(node.args, father)

        # 查找函数对象
        func_obj = father.fn_ctx[node.name]

        if not isinstance(func_obj, Func):
            func_obj(father, *args_list)
            return

        args_dict = {}

        for name, data in zip(func_obj.args, args_list):
            args_dict[name] = data
        func_obj.var_ctx = args_dict.copy()  # 参数
        func_obj.fn_ctx = father.fn_ctx  # 递归

        value = self.visits(func_obj.body, func_obj)
        if value:  # 有返回值
            value.reverse()
            father.stack += value

    def visits(self, items: list, father: Func | Root):
        for item in items:
            # item里是AST
            val = self.visit(item, father)
            if val:
                return val

    def try_pop(self, father: Root | Func):
        try:
            return father.stack.pop()
        except IndexError:
            return None
