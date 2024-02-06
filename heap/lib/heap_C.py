# Heap Lang
# chhongzh @ 2024

"""
使Heap支持动态.so与.dll
"""

from ctypes import CDLL, cdll
from ctypes import (
    c_bool,
    c_buffer,
    c_byte,
    c_char,
    c_char_p,
    c_double,
    c_float,
    c_int,
    c_int16,
    c_int32,
    c_int64,
    c_int8,
    c_long,
    c_longdouble,
    c_longlong,
    c_short,
    c_size_t,
    c_ssize_t,
    c_time_t,
    c_ubyte,
    c_uint,
    c_uint16,
    c_uint32,
    c_uint64,
    c_uint8,
    c_ulong,
    c_ulonglong,
    c_ushort,
    c_void_p,
    c_wchar,
    c_wchar_p,
)
from typing import Any

from ..asts import Func, Root
from ..log import module_info


class CLibrary:
    def __init__(self, cdll_object: CDLL):
        self._cdll_obj = cdll_object
        self._func_declared: dict[str, list[list, Any]] = (
            {}
        )  # 每个字典的键对应函数名, 字典对应的值是一个列表, 列表里有一个列表和一个返回值类型, 其中的列表是存储参数类型的.

    def set_func_ret(self, fn_name: str, fn_ret_type: Any):
        if fn_name not in self._func_declared:
            self._insert_struct(fn_name)

        self._cdll_obj[fn_name].restype = fn_ret_type
        self._func_declared[fn_name][1] = fn_ret_type

    def set_func_args(self, fn_name: str, fn_args_type: list[Any]):
        if fn_name not in self._func_declared:
            self._insert_struct(fn_name)

        self._func_declared[fn_name][0] = fn_args_type

    def _insert_struct(self, fn_name: str) -> None:
        self._func_declared[fn_name] = [[], None]

    def _before_call(self, fn_name: str):
        "检查是否定义返回值"
        if not (self._func_declared[fn_name][0] and self._func_declared[fn_name][1]):
            raise RuntimeError(
                f'Call method "{fn_name}", but never give argtype or retype'
            )

    def call(self, fn_name, *args, **kwargs):
        self._before_call(fn_name)

        c_fn = self._cdll_obj[fn_name]

        c_fn.restype = self._func_declared[fn_name][1]
        c_fn.argtypes = self._func_declared[fn_name][0]

        return c_fn(
            *args,
            **kwargs,
        )


def _cdll_loader(cdll_path: str) -> CDLL:
    module_info("C", f'准备加载文件: path="{cdll_path}"')

    _temp_cdll = cdll.LoadLibrary(cdll_path)

    module_info("C", "OK!")

    return _temp_cdll


def _c_load(father: Root | Func, path: str) -> CLibrary:
    cl = CLibrary(_cdll_loader(path))

    return cl


def _heap_init(father: Root | Func):
    father.context = {
        **father.context,
        **{  # 类型
            "C_bool": c_bool,
            "C_buffer": c_buffer,
            "C_byte": c_byte,
            "C_char": c_char,
            "C_char_p": c_char_p,
            "C_double": c_double,
            "C_float": c_float,
            "C_int": c_int,
            "C_int16": c_int16,
            "C_int32": c_int32,
            "C_int64": c_int64,
            "C_int8": c_int8,
            "C_long": c_long,
            "C_longdouble": c_longdouble,
            "C_longlong": c_longlong,
            "C_short": c_short,
            "C_size_t": c_size_t,
            "C_ssize_t": c_ssize_t,
            "C_time_t": c_time_t,
            "C_ubyte": c_ubyte,
            "C_uint": c_uint,
            "C_uint16": c_uint16,
            "C_uint32": c_uint32,
            "C_uint64": c_uint64,
            "C_uint8": c_uint8,
            "C_ulong": c_ulong,
            "C_ulonglong": c_ulonglong,
            "C_ushort": c_ushort,
            "C_void_p": c_void_p,
            "C_wchar": c_wchar,
            "C_wchar_p": c_wchar_p,
            "C_uint8": c_uint8,
            "C_ulong": c_ulong,
            "C_ulonglong": c_ulonglong,
            "C_ushort": c_ushort,
            "C_void_p": c_void_p,
            "C_wchar": c_wchar,
            "C_wchar_p": c_wchar_p,
        },
    }


def c_set_func_ret(father: Root | Func, cl: CLibrary, fn_name: str, type: Any):
    cl.set_func_ret(fn_name, type)


def c_set_func_args(father: Root | Func, cl: CLibrary, fn_name: str, *types):
    cl.set_func_args(fn_name, types)


def c_call(father: Root | Func, cl: CLibrary, fn_name: str, *args):
    return cl.call(fn_name, *args)


HEAP_EXPORT_FUNC = {
    "C_load": _c_load,
    "C_call": c_call,
    "C_set_func_args": c_set_func_args,
    "C_set_func_ret": c_set_func_ret,
}
