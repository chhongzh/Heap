from ..asts import Root, Func
from ..log import info


def length(father: Func | Root, val):
    father.stack.append(len(val))


def visit(father: Func | Root, val, idx: int | str):
    father.stack.append(val[idx])


HEAP_EXPORT_FUNC = {
    "length": length,
    "visit": visit,
}
