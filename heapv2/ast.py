from .common import get_type


class ASTNode:
    def __init__(self) -> None:
        raise NotImplementedError()

    def eval(
        self, runner, context: dict
    ) -> tuple[object, str]:  # 0: 返回的真实值, 1: 类型
        raise NotImplementedError()


class Return(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, runner, context: dict) -> tuple[object, str, bool]:
        e = self.expr
        if isinstance(e, (BoolExpr, BinExpr, Var, Call)):
            e = e.eval(runner, context)
            return e[0],e[1],True
        else:
            return e, get_type(e), True

    def __repr__(self) -> str:
        return f"Return({repr(self.expr)})"


class BoolExpr(ASTNode):
    def __init__(self, left, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BoolExpr({repr(self.left)}, {repr(self.op)}, {repr(self.right)})"

    def eval(self, runner, context: dict):
        rr_left = None
        rr_right = None
        if isinstance(self.left, (BinExpr, BoolExpr, Call, Var)):
            rr_left, _, brk_flag = self.left.eval(runner, context)
        else:
            rr_left = self.left
        if isinstance(self.right, (BinExpr, BoolExpr, Call, Var)):
            rr_right, _, brk_flag = self.right.eval(runner, context)
        else:
            rr_right = self.right

        match self.op:
            case "==":
                ll_val = rr_left == rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "!=":
                ll_val = rr_left != rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case ">=":
                ll_val = rr_left >= rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "<=":
                ll_val = rr_left <= rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case ">":
                ll_val = rr_left > rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "<":
                ll_val = rr_left < rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case _:
                raise RuntimeError(f"No op:{repr(self)}")


class BinExpr(ASTNode):
    def __init__(self, left, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinExpr({repr(self.left)}, {repr(self.op)}, {repr(self.right)})"

    def eval(self, runner, context: dict):
        rr_left = None
        rr_right = None
        if isinstance(self.left, (BinExpr, BoolExpr, Call, Var)):
            rr_left, _, brk = self.left.eval(runner, context)
        else:
            rr_left = self.left
        if isinstance(self.right, (BinExpr, BoolExpr, Call, Var)):
            rr_right, _, brk = self.right.eval(runner, context)
        else:
            rr_right = self.right

        match self.op:
            case "+":
                ll_val = rr_left + rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "-":
                ll_val = rr_left - rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "/":
                ll_val = rr_left / rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case "*":
                ll_val = rr_left * rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False
            case _:
                raise RuntimeError(f"No op:{repr(self)}")


class Call(ASTNode):
    def __init__(self, name: str, arg: list) -> None:
        self.name = name
        self.arg = arg

    def __repr__(self) -> str:
        return f"Call({repr(self.name)}, {repr(self.arg)})"

    def eval(self, runner, context: dict) -> tuple[object, str,bool]:
        # Eval arg:
        args = []
        for ll_arg in self.arg:
            if isinstance(ll_arg, (BinExpr, BoolExpr, Call, Var)):
                e=ll_arg.eval(runner, context)
                args.append(e[0])
            else:
                args.append(ll_arg)

        # Call FN
        
        if self.name not in context["object"]:
            raise RuntimeError("Not found or not callable!")
        if(context["typebound"][self.name] not in ('callable','py_callable')):
            raise RuntimeError(f"{context["typebound"][self.name]} is not a callable!")
        
        if(context["typebound"][self.name] == 'callable'): # Heap callable
            #ctx = {"object": {}, "typebound": {}}
            ctx = context.copy()
            fn_obj = context["object"][self.name]
            fn_obj: Func

            # 参数
            if len(args) != len(fn_obj.tb):
                raise RuntimeError("数量不匹配")

            for arg_in, arg_name, arg_type in zip(
                args, fn_obj.tb.keys(), fn_obj.tb.values()
            ):
                type = get_type(arg_in)
                if arg_type == type: # 不需要转换
                    ctx["object"][arg_name] = arg_in
                else:
                    if type == "int" and arg_type == "float":
                        ctx["object"][arg_name] = float(arg_in)
                    elif type == "float" and arg_type == "int":
                        ctx["object"][arg_name] = int(arg_in)
                    elif type == "bool" and arg_type == "int":
                        ctx["object"][arg_name] = int(arg_in)
                    elif type == "int" and arg_type == "bool":
                        ctx["object"][arg_name] = bool(arg_in)
                    elif type == "float" and arg_type == "bool":
                        ctx["object"][arg_name] = bool(arg_in)
                    elif type == "bool" and arg_type == "float":
                        ctx["object"][arg_name] = float(arg_in)
                    else:
                        raise RuntimeError(f"没有可以的cast(需要{arg_type}却给了{type})")
                ctx["typebound"][arg_name] = arg_type

            for statement in fn_obj.body:
                ll_val, ll_type, brk = statement.eval(runner, ctx)

                if brk:
                    type = get_type(ll_val)
                    if ll_type == type:
                        pass
                    elif type == "int" and ll_type == "float":
                        ll_val = float(ll_val)
                    elif type == "float" and ll_type == "int":
                        ll_val = int(ll_val)
                    elif type == "bool" and ll_type == "int":
                        ll_val = int(ll_val)
                    elif type == "int" and ll_type == "bool":
                        ll_val = bool(ll_val)
                    elif type == "float" and ll_type == "bool":
                        ll_val = bool(ll_val)
                    elif type == "bool" and ll_type == "float":
                        ll_val = float(ll_val)
                    else:
                        raise RuntimeError("没有可以的cast", ll_type, type)

                    return ll_val, ll_type, True
            return None,None,False
                
        elif(context["typebound"][self.name] == 'py_callable'):
            val = context["object"][self.name](runner,context,*args)
            return val,get_type(val),False

class VarDecl(ASTNode):
    def __init__(
        self, name: str, type: str, val: None | BinExpr | BoolExpr = None
    ) -> None:
        self.name = name
        self.type = type
        self.val = val

    def __repr__(self) -> str:
        return f"VarDecl({repr(self.name)}, {repr(self.type)}, {repr(self.val)})"

    def eval(self, runner, context: dict):
        if self.name in context:
            raise RuntimeError(f"Already Define :{self.name}")

        context["typebound"][self.name] = self.type
        if self.val != None:
            ll_value=self.val
            if(isinstance(self.val,(Var,Call,BoolExpr,BinExpr))):
                ll_value, ll_type, brk = self.val.eval(runner, context)
                if self.type == ll_type:
                    pass
                elif self.type == "int":
                    ll_value = int(ll_value)
                elif self.type == "float":
                    ll_value = float(ll_value)
                elif self.type == "bool":
                    ll_value = bool(ll_value)
                else:
                    raise TypeError(f"Can't Cast {ll_type} to {self.type}!")

            context["object"][self.name] = ll_value
        else:
            context["object"][self.name] = None

        return None, None, False


class Var(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Var({repr(self.name)})"

    def eval(self, runner, context: dict):
        return context["object"][self.name], context["typebound"][self.name], False


class Func(ASTNode):
    def __init__(self, type: str, name, tb: dict, body: list[ASTNode]) -> None:
        self.type = type
        self.name = name
        self.tb = tb
        self.body = body

    def __repr__(self) -> str:
        return f"Func({repr(self.type)}, {repr(self.name)}, {repr(self.tb)}, {repr(self.body)})"

    def eval(self, runner, ctx: dict):
        ctx["object"][self.name] = self
        ctx["typebound"][self.name] = "callable"

        return None, None, False


class VarSet(ASTNode):
    def __init__(self, name: str, expr: ASTNode) -> None:
        self.name = name
        self.expr = expr

    def __repr__(self) -> str:
        return f"VarSet({repr(self.name)}, {repr(self.expr)})"

    def eval(self, runner, ctx: dict):
        ctx["object"][self.name] = self.expr.eval(runner, ctx)[0]

        return None, None, False

"""
class Obj(ASTNode):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return str(self.obj)

    def eval(self, runner, ctx: dict):
        return self.obj, get_type(self.obj), False
"""

class If(ASTNode):
    def __init__(self,statements:list,exprs:list):
        self.statements=statements
        self.exprs=exprs

        self.has_else = len(self.statements)-1==len(self.exprs)

    def eval(self,runner,ctx):
        if(self.has_else):
            for statements,expr in zip(self.statements[:-1],self.exprs):
                if(expr.eval(runner,ctx)[0]):
                    for statement in statements:
                        ll_val,ll_type,brk = statement.eval(runner,ctx)

                        if(brk):
                            return ll_val,ll_type,brk
                    break
            else:
                for statement in self.statements[-1]:
                    ll_val,ll_type,brk = statement.eval(runner,ctx)

                    if(brk):
                        return ll_val,ll_type,brk
                   
        else:
            for statements,expr in zip(self.statements,self.exprs):
                if(expr.eval(runner,ctx)[0]):
                    for statement in statements:
                        ll_val,ll_type,brk = statement.eval(runner,ctx)

                        if(brk):
                            return ll_val,ll_type,brk
                    break

                
        return None,None,False

    def __repr__(self) -> str:
        return f"If({repr(self.statements)}, {repr(self.exprs)})"
