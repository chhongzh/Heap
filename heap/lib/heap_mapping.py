# Mapping 键值对
# chhongzh @ 2023 @ heap

from ..asts import Func, Root


def mapping(father: Root | Func):
    "Create a Map"

    father.stack.append({})


def set_key(_: Root | Func, mapping: dict, name: str, val):
    mapping[name] = val
    return mapping


def get_key(_: Root | Func, mapping: dict, name: str):
    return mapping[name]


def pop_key(_: Root | Func, mapping: dict, name: str):
    mapping.pop(name)

    return mapping


def get_keys(_: Root | Func, mapping: dict):
    return mapping.keys()


def get_values(_: Root | Func, mapping: dict):
    return mapping.values()


HEAP_EXPORT_FUNC = {
    "get_key": get_key,
    "get_keys": get_keys,
    "get_values": get_values,
    "mapping": mapping,
    "pop_key": pop_key,
    "set_key": set_key,
}
