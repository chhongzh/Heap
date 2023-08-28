# Chhongzh 2023
# Heap Lang
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
    While,
)
from os.path import exists, dirname, join
from inspect import isfunction
from . import hook
from .loader import loader
from . import Lexer, Builder
from .stdlibs import HEAP_LIBS, LIBS
from importlib import import_module
import sys
from os.path import split


class Runner:
    def __init__(self, root: Root, path: str):
        self.root = root
        self.include_path = [path]

    def run(self):
        """运行"""

        # 魔法变量:
        self.root.var_ctx["__heap_excutable"] = sys.executable
        self.root.var_ctx["__heap_argv"] = sys.argv[1:]

        self.visits(self.root.body, self.root)

    def visit(self, node, father: Root | Func):
        """解析一个Node"""
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
        elif isinstance(node, While):
            self.expr_while(node, father)
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
        """加载一个模块"""
        if path in LIBS:  # 对于是Python文件的模块
            md = import_module(f".lib.{LIBS[path]}", "heap")
            for name in md.__dir__():
                if (
                    not name.startswith("__")
                    and not name.endswith("__")
                    and isfunction(md.__dict__[name])
                ):
                    father.fn_ctx[name] = md.__dict__[name]
            return
        elif path in HEAP_LIBS:  # 对于是Heap文件的模块
            content = loader(join(split(__file__)[0], "lib", HEAP_LIBS[path]))
            lexer = Lexer(content)
            toks = lexer.lex()

            builder = Builder(toks)
            ast = builder.parse()
            self.visits(ast.body, father)

            return

        path = join(self.include_path[-1], path)
        self.include_path.append(dirname(path))  # 将解析目录加入到栈

        if not exists(path):
            hook._raise_error(IncludeError(path, -1, "Not a file."))
            return

        content = loader(path)
        lexer = Lexer(content)
        toks = lexer.lex()

        builder = Builder(toks)
        ast = builder.parse()
        self.visits(ast.body, father)

        self.include_path.pop()  # 弹出

    def expr_args(self, args: list, father: Func | Root, delete=True):
        """解析函数参数"""

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

                    if op == "equal" and l1 == l2:
                        self.visits(body, father)
                        break
                    elif op == "bigequal" and l1 >= l2:
                        self.visits(body, father)
                        break
                    elif op == "small" and l1 < l2:
                        self.visits(body, father)
                        break
                    elif op == "big" and l1 > l2:
                        self.visits(body, father)
                        break
                    elif op == "smallequal" and l1 <= l2:
                        self.visits(body, father)
                        break
                    elif op == "notequal" and l1 != l2:
                        self.visits(body, father)
                        break
                else:
                    self.visits(node.bodys[-1], father)

            elif len(node.l1s) == len(node.bodys):
                for l1, op, l2, body in zip(node.l1s, node.ops, node.l2s, node.bodys):
                    l1, op, l2 = self.expr_args([l1, op, l2], father, False)

                    if op == "equal" and l1 == l2:
                        self.visits(body, father)
                        break
                    elif op == "bigequal" and l1 >= l2:
                        self.visits(body, father)
                        break
                    elif op == "small" and l1 < l2:
                        self.visits(body, father)
                        break
                    elif op == "smallequal" and l1 <= l2:
                        self.visits(body, father)
                        break
                    elif op == "notequal" and l1 != l2:
                        self.visits(body, father)
                        break
                    elif op == "big" and l1 > l2:
                        self.visits(body, father)
                        break
                else:
                    self.visits(node.bodys[-1], father)
            else:
                raise Exception(len(node.l1s), len(node.bodys))

    def expr_while(self, node: While, father: Root | Func):
        temp = self.expr_args([node.expr1, node.op, node.expr2], father, False)
        expr1 = temp[0]
        op = temp[1]
        expr2 = temp[2]

        if op == "notequal":
            while expr1 != expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "equal":
            while expr1 == expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "small":
            while expr1 < expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "smallequal":
            while expr1 <= expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

        elif op == "bigequal":
            while expr1 >= expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

        elif op == "big":
            while expr1 > expr2:
                self.visits(node.body, father)
                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

    def call(self, node: Call, father: Root | Func):
        if node.name in father.command:  # 指令不能有参数
            if node.args:
                raise Exception

            self.visits(father.command[node.name].body, father)
            return

        args_list = self.expr_args(node.args, father)

        # 查找函数对象
        if node.name not in father.fn_ctx:
            hook._raise_error(NotDefine(node.name, -1))
            return

        func_obj = father.fn_ctx[node.name]

        if not isinstance(func_obj, Func):
            func_obj(father, *args_list)  # 如果是Python Function
            return

        args_dict = {}  # 解析数据
        for name, data in zip(func_obj.args, args_list):
            args_dict[name] = data
        func_obj.var_ctx = args_dict.copy()  # 参数
        func_obj.fn_ctx = father.fn_ctx  # 递归

        value = self.visits(func_obj.body, func_obj)
        if value:  # 有返回值
            value.reverse()
            father.stack += value

    def visits(self, items: list, father: Func | Root):
        """递归遍历所有nodes"""
        for item in items:
            # item里是AST
            val = self.visit(item, father)
            if val:  # 处理返回值
                return val

    def try_pop(self, father: Root | Func):
        try:
            return father.stack.pop()
        except IndexError:
            return None
