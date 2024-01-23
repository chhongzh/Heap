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
    # 下面的函数名称将会被弃用
    "capitalize": lambda *args, **kwargs: (
        print("[String]: 函数capitalize将会在V1.6.0中移除, 请使用string_capitalize!"),
        capitalize(*args, **kwargs),
    )[1],
    "count": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数count将会在V1.6.0中移除, 请使用string_count!"),
        count(*args, **kwargs),
    )[1],
    "decode": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数decode将会在V1.6.0中移除, 请使用string_decode!"),
        decode(*args, **kwargs),
    )[1],
    "lower": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数lower将会在V1.6.0中移除, 请使用string_lower!"),
        lower(*args, **kwargs),
    )[1],
    "replace": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数replace将会在V1.6.0中移除, 请使用string_replace!"),
        replace(*args, **kwargs),
    )[1],
    "replace_count": lambda *args, **kwargs: (
        print(
            "[Deprecate!]: [string]: 函数replace_count将会在V1.6.0中移除, 请使用string_replace_count!"
        ),
        replace_count(*args, **kwargs),
    )[1],
    "swapcase": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数swapcase将会在V1.6.0中移除, 请使用string_swapcase!"),
        swapcase(*args, **kwargs),
    )[1],
    "title": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数title将会在V1.6.0中移除, 请使用string_title!"),
        title(*args, **kwargs),
    )[1],
    "upper": lambda *args, **kwargs: (
        print("[Deprecate!]: [string]: 函数upper将会在V1.6.0中移除, 请使用string_upper!"),
        upper(*args, **kwargs),
    )[1],
    "string_capitalize": capitalize,
    "string_count": count,
    "string_decode": decode,
    "string_lower": lower,
    "string_replace": replace,
    "string_replace_count": replace_count,
    "string_swapcase": swapcase,
    "string_title": title,
    "string_upper": upper,
}
