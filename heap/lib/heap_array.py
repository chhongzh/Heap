from ..asts import Root, Func


def array(father: Func | Root):
    father.stack.append([])


def array_pop(father: Func | Root, lst: list, idx=-1):
    return lst.pop(idx)


def array_append(father: Func | Root, lst: list, val):
    lst.append(val)
    return lst


def array_del(father: Func | Root, lst: list, idx: int):
    del lst[idx]
    return lst


HEAP_EXPORT_FUNC = {
    "array": array,
    "array_append": array_append,
    "array_pop": array_pop,
    "array_del": array_del,
}
