from heap.asts import Root, Func


def array(father: Func | Root):
    father.stack.append([])


def array_pop(father: Func | Root, lst: list):
    return lst.pop()


def array_append(father: Func | Root, lst: list, val):
    lst.append(val)
    return lst
