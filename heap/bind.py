from inspect import isfunction
from .common import get_type


def bind_from_module(
    ctx: dict,
    module: dict,
    ignore_prefix=("__", "_"),
    add_prefix="",
    force_callable: bool = False,
    re_write_method: bool = False,
    ignore: list = [],
):
    for kw_name in module.__dir__():
        if kw_name in ignore:
            continue
        if not kw_name.startswith(ignore_prefix):
            O = module.__getattribute__(kw_name)
            if kw_name in ctx["object"]:
                continue
            if force_callable:
                ctx["typebound"][add_prefix + kw_name] = "py_callable"
            else:

                if isfunction(O):
                    ctx["typebound"][add_prefix + kw_name] = "py_callable"
                else:
                    ctx["typebound"][add_prefix + kw_name] = get_type(O)

            if re_write_method:
                ctx["object"][add_prefix + kw_name] = lambda runner, ctx, *args: O(
                    *args
                )
            else:
                ctx["object"][add_prefix + kw_name] = O
