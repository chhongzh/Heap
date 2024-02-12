from ..asts import Root, Func
from ..log import info


def length(father: Func | Root, val):
    father.stack.append(len(val))


def visit(father: Func | Root, val, idx: int | str):
    father.stack.append(val[idx])


def format(father: Func | Root, val: str, *args):
    return val % args


def format_list(father: Func | Root, val: str, args: tuple):
    return val % tuple(args)


def arg(father: Root | Func, *args):
    return args


HEAP_EXPORT_FUNC = {
    "length": length,
    "visit": visit,
    "format": format,
    "format_list": format_list,
    "arg": arg,
}
