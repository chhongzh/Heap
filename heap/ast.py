from .common import get_type, go_C
from os import get_terminal_size

CPP_TYPE_TABLE={'int':'Int','string':'String','void':'Void','float':'Float'}



class ASTNode:
    def __init__(self) -> None:
        raise NotImplementedError()

    def eval(
        self, runner, context: dict
    ) -> tuple[object, str,bool,int]:  # 0: 返回的真实值, 1: 类型, 2: 是否return 3: (1: conntinue, 2: break , 0: nothing)
        """用于执行AST"""
        raise NotImplementedError()
    
    def trans_C(self) -> str: 
        """返回一个C语句"""

        raise NotImplementedError()

    def translate_log(self,msg:str):
        width = get_terminal_size()[0]
        left = f"[{self.__class__.__name__}][Frontend]"
        right = msg
        space_cnt = width-(len(left)+len(right))
        if(space_cnt >= 0):
            print(f'{right}{" "*space_cnt}{left}')
        else:
            print(f'{right[:space_cnt-3]}...{left}')


class Return(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, runner, context: dict) -> tuple[object, str, bool]:
        e = (self.expr)
        if isinstance(e, (BoolExpr, BinExpr, Var, Call)):
            e = e.eval(runner, context)
            return e[0],e[1],True,0
        else:
            return e, get_type(e), True,0

    def __repr__(self) -> str:
        return f"Return({repr(self.expr)})"
    
    def trans_C(self) -> str:
        C_string :str
        if(isinstance(self.expr,ASTNode)):
            self.translate_log(f'↓ Translate child.')
            C_string = self.expr.trans_C()
        else:
            C_string = go_C(self.expr)
        self.translate_log(f'↑ Okay')
        return f"return {C_string}"


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
            rr_left, _, brk_flag,ctn_or_brk = self.left.eval(runner, context)
        else:
            rr_left = (self.left)
        if isinstance(self.right, (BinExpr, BoolExpr, Call, Var)):
            rr_right, _, brk_flag,ctn_or_brk = self.right.eval(runner, context)
        else:
            rr_right = (self.right)

        match self.op:
            case "==":
                ll_val = rr_left == rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "!=":
                ll_val = rr_left != rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case ">=":
                ll_val = rr_left >= rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "<=":
                ll_val = rr_left <= rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case ">":
                ll_val = rr_left > rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "<":
                ll_val = rr_left < rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case _:
                raise RuntimeError(f"No op:{repr(self)}")
            
    def trans_C(self) -> str:
        C_left_string :str
        C_right_string:str
        if(isinstance(self.left,ASTNode)):
            self.translate_log(f'↓ Translate child.')
            C_left_string = self.left.trans_C()
        else:
            C_left_string = go_C(self.left)

        if(isinstance(self.right,ASTNode)):
            self.translate_log(f'↓ Translate child.')
            C_right_string = self.right.trans_C()
        else:
            C_right_string = go_C(self.right)
        self.translate_log(f'↑ Okay')
        return f"{C_left_string} {self.op} {C_right_string}"

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
            rr_left, _, brk,__ = self.left.eval(runner, context)
        else:
            rr_left = (self.left)
        if isinstance(self.right, (BinExpr, BoolExpr, Call, Var)):
            rr_right, _, brk,__ = self.right.eval(runner, context)
        else:
            rr_right = (self.right)

        match self.op:
            case "+":
                ll_val = rr_left + rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "-":
                ll_val = rr_left - rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "/":
                ll_val = rr_left / rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case "*":
                ll_val = rr_left * rr_right
                ll_type = get_type(ll_val)
                return ll_val, ll_type, False,0
            case _:
                raise RuntimeError(f"No op:{repr(self)}")
            
    def trans_C(self) -> str:
        C_left_string :str
        C_right_string:str
        if(isinstance(self.left,ASTNode)):
            self.translate_log(f'↓ Translate child.')
            C_left_string = self.left.trans_C()
        else:
            C_left_string = go_C(self.left)

        if(isinstance(self.right,ASTNode)):
            self.translate_log(f'↓ Translate child.')
            C_right_string = self.right.trans_C()
        else:
            C_right_string = go_C(self.right)

        self.translate_log(f'← Ok with "{C_left_string} {self.op} {C_right_string}"')
        return f"{C_left_string} {self.op} {C_right_string}"

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
                args.append((e[0]))
            else:
                args.append((ll_arg))

        # Call FN
        
        if self.name not in context["object"]:
            raise RuntimeError(f"Not found or not callable!, {self.name}")
        if(context["typebound"][self.name] not in ('callable','py_callable',
                                                   'builtin_function_or_method', # Fix call error
                                                   )):
            raise RuntimeError(f"{context["typebound"][self.name]} is not a callable!")
        
        if(context["typebound"][self.name] == 'callable'): # Heap callable
            #ctx = {"object": {}, "typebound": {}}
            ctx = {}
            ctx['object'] = (context['object'].copy())
            ctx['typebound'] = (context['typebound'].copy())
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
                ll_val, ll_type, brk,ctn_or_brk = statement.eval(runner, ctx)

                if ctn_or_brk!=0:
                    return None,None,False,ctn_or_brk

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

                    return ll_val, ll_type, True,0
                
            return None,None,False,0
                
        elif(context["typebound"][self.name] in ('py_callable','builtin_function_or_method')):
            val = context["object"][self.name](runner,context,*args)
            return val,get_type(val),False,0
    
    def trans_C(self) -> str:
        self.translate_log(f'↓ Translate child.')
        self.translate_log(f'↑ Okay')
        return f"{self.name}({', '.join([i.trans_C() if isinstance(i,ASTNode) else go_C(i) for i in self.arg])})"

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
                ll_value, ll_type, brk,_ = self.val.eval(runner, context)
                if self.type == ll_type:
                    pass
                elif self.type == "int":
                    ll_value = int(ll_value)
                elif self.type == "float":
                    ll_value = float(ll_value)
                elif self.type == "bool":
                    ll_value = bool(ll_value)
                else:
                    raise RuntimeError(f"Can't Cast {ll_type} to {self.type}!")

            context["object"][self.name] = ll_value
        else:
            context["object"][self.name] = None

        return None, None, False,0
    
    def trans_C(self) -> str:
        if(self.val != None):
            val = self.val
            if(isinstance(self.val,ASTNode)):
                self.translate_log(f'↓ Translate child.')
                val = self.val.trans_C()
            else:
                val = go_C(val)
            self.translate_log(f'↑ Okay')
            return f"{CPP_TYPE_TABLE[self.type]} {self.name} = {val}"
        else:
            self.translate_log(f'↑ Okay')
            return f"{CPP_TYPE_TABLE[self.type]} {self.name}"


class Var(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Var({repr(self.name)})"

    def eval(self, runner, context: dict):
        return (context["object"][self.name]), (context["typebound"][self.name]), False,0

    def trans_C(self) -> str:
        self.translate_log(f'↑ Okay')
        return f"{self.name}"

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

        return None, None, False,0

    def trans_C(self) -> str:
        C_body = []
        for stmt in self.body:
            C_body.append(stmt.trans_C())
        self.translate_log(f'↑ Okay')
        return f"auto {self.name} = []({', '.join([CPP_TYPE_TABLE[type]+' '+name for name,type in self.tb.items()])}){{ {''.join([x+"; " for x in C_body])} }}"

class VarSet(ASTNode):
    def __init__(self, name: str, expr: ASTNode) -> None:
        self.name = name
        self.expr = expr

    def __repr__(self) -> str:
        return f"VarSet({repr(self.name)}, {repr(self.expr)})"

    def eval(self, runner, ctx: dict):
        if(isinstance(self.expr,(BinExpr,BoolExpr,Call,Var))):
            ll_val,ll_type,_,__=self.expr.eval(runner, ctx)

            # Type Convert
            if ctx["typebound"][self.name] == ll_type:
                pass
            elif ctx["typebound"][self.name] == "int":
                ll_val = int(ll_val)
            elif ctx["typebound"][self.name] == "float":
                ll_val = float(ll_val)
            elif ctx["typebound"][self.name] == "bool":
                ll_val = bool(ll_val)
            else:
                raise RuntimeError(f"Can't Cast {ll_type} to {ctx["typebound"][self.name]}!")
            ctx["object"][self.name] = ll_val
        else:
            ll_val=self.expr

            # Type Covert
            if ctx["typebound"][self.name] == get_type(ll_val):
                pass
            elif ctx["typebound"][self.name] == "int":
                ll_val = int(ll_val)
            elif ctx["typebound"][self.name] == "float":
                ll_val = float(ll_val)
            elif ctx["typebound"][self.name] == "bool":
                ll_val = bool(ll_val)
            else:
                raise RuntimeError(f"Can't Cast {ll_type} to {ctx["typebound"][self.name]}!")
            ctx["object"][self.name] = ll_val

        return None, None, False,0
    
    def trans_C(self) -> str:
        self.translate_log(f'↓ Translate child.')
        self.translate_log(f'↑ Okay')
        return f"{self.name} = {self.expr.trans_C() if isinstance(self.expr,(ASTNode)) else go_C(self.expr)}"

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
                        ll_val,ll_type,brk,ctn_or_brk = statement.eval(runner,ctx)

                        if ctn_or_brk!=0:
                            return None,None,False,ctn_or_brk

                        if(brk):
                            return ll_val,ll_type,brk
                    break
            else:
                for statement in self.statements[-1]:
                    ll_val,ll_type,brk,ctn_or_brk = statement.eval(runner,ctx)

                    if ctn_or_brk!=0:
                        return None,None,False,ctn_or_brk

                    if(brk):
                        return ll_val,ll_type,brk,0
                   
        else:
            for statements,expr in zip(self.statements,self.exprs):
                if(expr.eval(runner,ctx)[0]):
                    for statement in statements:
                        ll_val,ll_type,brk,ctn_or_brk = statement.eval(runner,ctx)

                        if ctn_or_brk!=0:
                            return None,None,False,ctn_or_brk

                        if(brk):
                            return ll_val,ll_type,brk,0
                    break

                
        return None,None,False,0

    def __repr__(self) -> str:
        return f"If({repr(self.statements)}, {repr(self.exprs)})"

    def trans_C(self) -> str:
        C_exprs = []
        C_stmt = []
        C_str=""

        for exprs in self.exprs:
            C_exprs . append( exprs.trans_C() if isinstance(exprs,(Var,BinExpr,BoolExpr,Call)) else go_C(exprs) )
        
        for C_s in self.statements:
            C_temp = []
            for exprs in C_s:
                self.translate_log(f'↓ Translate child.')
                C_temp.append(exprs.trans_C() if isinstance(exprs,ASTNode) else go_C(exprs))
            C_stmt.append(' '.join([x+';' for x in C_temp]))

        if(self.has_else):
            dd_word = 'if'
            for expr,stmt in zip(C_exprs,C_stmt[:-1]):
                C_str+=f"{dd_word}({expr}){{ {stmt} }}"
                dd_word='else if'
            C_str+=f"else{{ {C_stmt[-1]} }}"
        else:
            dd_word = 'if'
            for expr,stmt in zip(C_exprs,C_stmt):
                C_str+=f"{dd_word}({expr}){{ {stmt} }}"
                dd_word='else if'

        self.translate_log(f'↑ Okay')
        return C_str
            
class While(ASTNode):
    def __init__(self,statements:list,expr):
        self.statements=statements
        self.expr=expr


    def eval(self,runner,ctx):
        while True:
            if(isinstance(self.expr,(BinExpr,BoolExpr,Call,Var))):
                ll_flag,ll_type,_,__=self.expr.eval(runner,ctx)
            else:
                ll_flag = self.expr
            if(not ll_flag):
                break
            
            rr_type = 0

            for stmt in self.statements:
                ll_val,ll_type,brk,ctn_or_brk=stmt.eval(runner,ctx)

                if(ctn_or_brk==1):
                    rr_type = ctn_or_brk
                    break
                elif (ctn_or_brk == 2):
                    rr_type = ctn_or_brk
                    break

                if(brk):
                    return ll_val,ll_type,brk,0
            if(rr_type==1):
                continue
            elif(rr_type==2):
                break
        return None,None,False,0

    def __repr__(self) -> str:
        return f"While({repr(self.statements)}, {repr(self.expr)})"

    def trans_C(self) -> str:
        C_body = []
        self.translate_log(f'↓ Translate child.')
        C_statement  = self.expr.trans_C() if isinstance(self.expr,ASTNode) else go_C(self.expr)

        for stmt in self.statements:
            C_body.append(stmt.trans_C())
        
        self.translate_log(f'↑ Okay')
        return f"while ( {C_statement} ){{ {''.join([x+';' for x in C_body])} }}"

class Break(ASTNode):
    def __init__(self):
        ...

    def eval(self,runner,ctx):
        return None,None,False,2

    def __repr__(self) -> str:
        return f"Break()"

    def trans_C(self) -> str:
        self.translate_log('↑ Okay')
        return "break"
class Continue(ASTNode):
    def __init__(self):
        ...

    def eval(self,runner,ctx):
        return None,None,False,1

    def __repr__(self) -> str:
        return f"Continue()"

    def trans_C(self) -> str:
        self.translate_log('↑ Okay')
        return "continue"
