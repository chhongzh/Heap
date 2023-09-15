from heap.asts import Root, Func


def arraypop(father: Func | Root, lst: list):
    lst.pop()


def arrayappend(father: Func | Root, lst: list, val):
    lst.append(val)
