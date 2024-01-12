from ..asts import Func, Root


def lower(father: Root | Func, val: str):
    return val.lower()


def upper(father: Root | Func, val: str):
    return val.upper()


def title(father: Root | Func, val: str):
    return val.title()


def capitalize(father: Root | Func, val: str):
    return val.capitalize()


def swapcase(father: Root | Func, val: str):
    return val.swapcase()


def replace(father: Root | Func, val: str, old: str, new: str):
    return val.replace(old, new)


def replace_count(father: Root | Func, val: str, old: str, new: str, count: int):
    return val.replace(old, new, count)


def count(father: Root | Func, val: str, o: str):
    return val.count(o)


def decode(father: Root | Func, val: bytes, encoding: str):
    return val.decode(encoding)


HEAP_EXPORT_FUNC = {
    "capitalize": capitalize,
    "count": count,
    "decode": decode,
    "lower": lower,
    "replace": replace,
    "replace_count": replace_count,
    "swapcase": swapcase,
    "title": title,
    "upper": upper,
}
