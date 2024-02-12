from inspect import isfunction
from .common import get_type


def bind_from_module(ctx: dict, module: dict, ignore_prefix=("__", "_"), add_prefix=""):
    for kw_name in module.__dir__():
        if not kw_name.startswith(ignore_prefix):
            O = module.__getattribute__(kw_name)
            if isfunction(O):
                ctx["typebound"][add_prefix + kw_name] = "py_callable"
            else:
                ctx["typebound"][add_prefix + kw_name] = get_type(O)

            ctx["object"][add_prefix + kw_name] = O
