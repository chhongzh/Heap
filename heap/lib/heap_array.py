from ..asts import Root, Func


def array(father: Func | Root):
    father.stack.append([])


def array_pop(father: Func | Root, lst: list):
    return lst.pop()


def array_append(father: Func | Root, lst: list, val):
    lst.append(val)
    return lst


HEAP_EXPORT_FUNC = {
    "array": array,
    "array_append": array_append,
    "array_pop": array_pop,
}
