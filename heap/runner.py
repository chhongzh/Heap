# Chhongzh 2023
# Heap Lang

"""
Heap的运行器,
运行一段ast
"""

import sys
from importlib import import_module
from inspect import isfunction
from os.path import exists, dirname, join, split, isfile, isdir
from .log import info, debug, critical, error

from .error import (
    BaseError,
    BuilderErr,
    CallErr,
    IncludeError,
    NotDefine,
    PopFromEmptyStack,
)
from .asts import (
    Div,
    Input,
    LinkExpr,
    Mul,
    Node,
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
    Iter,
)
from .loader import loader
from .stdlibs import HEAP_LIBS, LIBS
from . import Lexer, Builder
from . import hook


class Runner:
    """Heap 解析器"""

    def __init__(self, root: Root, path: str, need_inject_module=True):
        """
        传入一个Root节点, 并运行

        path : 导入路径
        root : 根节点
        """

        self.root = root
        self.include_path = [path]
        # Running Blobk - 记录当前块
        self.running_block = []

        if need_inject_module:
            self.load_module("builtin", self.root)  # 注入内建库
            self.load_module("_py_builtin", self.root)  # 注入内建库

        # 魔法变量:
        self.root.var_ctx["heap_excutable"] = sys.executable
        self.root.var_ctx["heap_argv"] = []

        self.root.runner = self  # 注入自己

        info("[Runner]: 就绪")

    def run(self):
        """运行"""

        info("[Runner]: 开始运行")
        self.visits(self.root.body, self.root)
        info("[Runner]: 结束运行")

    def visit(self, node, father: Root | Func):
        """解析一个Node"""

        # 添加到Running_Block
        self.running_block.append(node.__class__.__name__)

        if isinstance(node, Func):
            self.running_block[-1] = f"Defining Func {node.name}"
            father.var_ctx[node.name] = node
        elif isinstance(node, Input):
            father.stack.append(input(self.expr_args([node.val], father)[0]))
        elif isinstance(node, Command):
            father.command[node.name] = node
        elif isinstance(node, Set):
            father.var_ctx[node.name] = self.expr_args([node.val], father)[0]
        elif isinstance(node, Get):
            self.running_block[-1] = f'Get "{node.name}"'

            self.expr_get(node, father)
        elif isinstance(node, Push):
            father.stack.append(node.val)
        elif isinstance(node, Pop):
            self.try_pop(father)
        elif isinstance(node, Print):
            hook.print_val(self.try_pop(father))
        elif isinstance(node, Call):
            self.running_block[-1] = f'Calling "{node.name}"'

            self.call(node, father)
        elif isinstance(node, While):
            # While 也有可能会有返回值
            return self.expr_while(node, father)
        elif isinstance(node, Return):
            dt = self.expr_args(node.vals, father)
            info(f"[Runner]: 返回值:({dt})")

            # 别忘记在Return 之前删除
            self.running_block.pop()

            return dt
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
            # If可能会有返回值(return打断)
            return self.expr_if(node, father)
        elif isinstance(node, Include):
            self.load_module(node.path, father)
        elif isinstance(node, Iter):
            # Return 打断
            return self.expr_iter(node, father)
        elif isinstance(node, LinkExpr):
            self.expr_link(node, father)

        self.running_block.pop()

    def expr_get(self, node: Get, father: Root | Func):
        if node.name not in father.var_ctx.keys():
            self.hook_raise_error(NotDefine(f"变量:{node.name}, 并未创建, 但却被访问了", -1))
        father.stack.append(father.var_ctx[node.name])

    def expr_link(self, node: LinkExpr, father: Root | Func):
        """解析Link语句"""

        info("[Runner]: 准备匹配link-expr表达式")

        root_value = self.expr_args([node.value], father)[0]

        for fn_name, fn_val in zip(node.call_chain, node.arg_chain):
            self.call(Call(fn_name, [root_value, *fn_val]), father)

            if len(root_value) > 0:
                root_value = father.stack.pop()
                info(f"[Runner]: 结果:{repr(root_value)[0:5]}...")
            else:
                info(f"[Runner]: 没有返回值")

        if root_value:
            father.stack.append(root_value)  # 别忘了将最终结果返回去

    def load_module(self, path: str, father: Func | Root):
        """加载一个模块"""

        info(f"[Runner]: 加载模块:{path}")

        if path in LIBS:  # 对于是Python文件的模块
            info("[Runner]: [Heap-Bridge]: 导入来自Python的模块")

            module = import_module(f".lib.{LIBS[path]}", "heap")
            for name in dir(module):
                if (
                    not name.startswith("__")
                    and not name.endswith("__")
                    and isfunction(module.__dict__[name])
                    and name != "_heap_init"
                ):
                    info(f"[Runner]: [Heap-Bridge]: 注册函数: Name:{name}")
                    father.var_ctx[name] = module.__dict__[name]
            if "_heap_init" in dir(module):
                info(f"[Runner]: [Heap-Bridge]: 在模块中找到钩子init, 调用")

                module.__dict__["_heap_init"](father)

            return
        if path in HEAP_LIBS:  # 对于是Heap文件的模块
            file_path = join(split(__file__)[0], "lib", HEAP_LIBS[path])

            content = loader(file_path)
            lexer = Lexer(content)
            toks = lexer.lex()

            builder = Builder(toks)
            ast = builder.parse()
            self.visits(ast.body, father)

            return

        path = join(self.include_path[-1], path)
        self.include_path.append(dirname(path))  # 将解析目录加入到栈
        info(f"[Runner]: 尝试打开{path}")

        if isdir(path) or not isfile(path):
            error("[Runner]: 路径不正确")
            self.hook_raise_error(IncludeError(path, -1, "Not a file."))
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

        info(f"[Runner]: 准备解析参数. Count:{len(args)}")
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
        "解析if语句"

        if not len(node.l1s) == len(node.l2s) == len(node.ops):
            hook.print_error(BuilderErr("", -1, "数量不对"))

        else:
            # if-else mode:
            if len(node.l1s) + 1 == len(node.bodys):
                return_value = None

                for l1, op, l2, body in zip(
                    node.l1s, node.ops, node.l2s, node.bodys[:-1]
                ):
                    temp_data = self.expr_args([l1, op, l2], father, False)
                    l1 = temp_data[0]
                    op = temp_data[1]
                    l2 = temp_data[2]

                    if op == "equal" and l1 == l2:
                        return self.visits(body, father)

                    if op == "bigequal" and l1 >= l2:
                        return self.visits(body, father)

                    if op == "small" and l1 < l2:
                        return self.visits(body, father)

                    if op == "big" and l1 > l2:
                        return self.visits(body, father)

                    if op == "smallequal" and l1 <= l2:
                        return self.visits(body, father)

                    if op == "notequal" and l1 != l2:
                        return self.visits(body, father)

                    return self.visits(node.bodys[-1], father)

            elif len(node.l1s) == len(node.bodys):
                for l1, op, l2, body in zip(node.l1s, node.ops, node.l2s, node.bodys):
                    temp_data = self.expr_args([l1, op, l2], father, False)
                    l1 = temp_data[0]
                    op = temp_data[1]
                    l2 = temp_data[2]

                    if op == "equal" and l1 == l2:
                        return self.visits(body, father)

                    if op == "bigequal" and l1 >= l2:
                        return self.visits(body, father)

                    if op == "small" and l1 < l2:
                        return self.visits(body, father)

                    if op == "smallequal" and l1 <= l2:
                        return self.visits(body, father)

                    if op == "notequal" and l1 != l2:
                        return self.visits(body, father)

                    if op == "big" and l1 > l2:
                        return self.visits(body, father)

                # self.visits(node.bodys[-1], father) : 修复错误, 这一行是多余的
            else:
                hook.print_error(BuilderErr("", -1, "未知的错误"))

    def expr_while(self, node: While, father: Root | Func):
        "解析while语句"

        temp = self.expr_args([node.expr1, node.op, node.expr2], father, False)
        expr1 = temp[0]
        op = temp[1]
        expr2 = temp[2]

        if op == "notequal":
            while expr1 != expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "equal":
            while expr1 == expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "small":
            while expr1 < expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]
        elif op == "smallequal":
            while expr1 <= expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

        elif op == "bigequal":
            while expr1 >= expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

        elif op == "big":
            while expr1 > expr2:
                ret_val = self.visits(node.body, father)
                if ret_val != None:
                    return ret_val

                temp = self.expr_args([node.expr1, node.expr2], father)
                expr1 = temp[0]
                expr2 = temp[1]

    def call(self, node: Call, father: Root | Func):
        "调用一个函数"

        if node.name in father.command:  # 指令不能有参数
            if node.args:
                hook.print_error(CallErr(node.name, -1, "调用command不能有参数"))

            self.visits(father.command[node.name].body, father)
            return

        args_list = self.expr_args(node.args, father)

        # 查找函数对象
        if node.name not in father.var_ctx:
            self.hook_raise_error(NotDefine(node.name, -1))
            return

        func_obj = father.var_ctx[node.name]

        if isfunction(func_obj):
            value = func_obj(father, *args_list)  # 如果是Python Function
            if value != None:
                father.stack.append(value)
            return

        args_dict = {}  # 解析数据
        for name, data in zip(func_obj.args, args_list):
            args_dict[name] = data

        func_obj.var_ctx.clear()  # 清除所有的记录
        return_var_name = []  # 记录返回之后的变量

        # 传入了参数但是全局变量没有传入

        for var_name in father.var_ctx:
            var_name: str
            if var_name.isupper():
                func_obj.var_ctx = father.var_ctx[var_name]
                return_var_name.append(var_name)

        func_obj.var_ctx = {**father.var_ctx, **args_dict.copy()}  # 参数

        func_obj.stack.clear()  # 清空stack

        value = self.visits(func_obj.body, func_obj)

        info("[Runner]: 存储全局")
        for var_name in return_var_name:
            father.var_ctx[var_name] = func_obj.var_ctx[var_name]

        if value:  # 有返回值
            value.reverse()
            info(f"[Runner]: 调用函数:{node.name}, 返回:{value}")
            father.stack += value

    def visits(self, items: list, father: Func | Root):
        """递归遍历所有nodes"""
        for item in items:
            # item里是AST
            val = self.visit(item, father)
            if val:  # 处理返回值
                return val

    def try_pop(self, father: Root | Func, raise_err: bool = True):
        "尝试获取一个堆栈数据"

        try:
            return father.stack.pop()
        except IndexError:
            if raise_err:
                self.hook_raise_error(PopFromEmptyStack("尝试从空栈中获取数据.", -1))
            return None

    def expr_iter(self, node: Iter, father: Root | Func):
        "解析iter语句"

        iter_name = node.iter_name

        val = self.expr_args([node.val], father)[0]

        for i in val:
            father.var_ctx[iter_name] = i  # Bound the varibles
            ret_val = self.visits(node.body, father)  # 调用代码

            if ret_val != None:
                return ret_val

    def hook_raise_error(self, error: BaseError):
        print("Traceback: On running code, but error was generated.")
        print(f'On file: "{self.root.file_path}"')
        for name in self.running_block:
            print(f"  At Statement:{name}")
        hook.raise_error(error)
