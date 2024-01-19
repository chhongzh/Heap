# Heap @ 2024
# Base64 lib

"""
Base 64, 
提供编解码函数
"""

from ..asts import Root, Func
from base64 import b64decode, b64encode


def base64_encode(father: Root | Func, value: str) -> str:
    return b64encode(value.encode()).decode()


def base64_decode(father: Root | Func, value: str) -> str:
    return b64decode(value).decode()


HEAP_EXPORT_FUNC = {
    "base64_encode": base64_encode,
    "base64_decode": base64_decode,
}

# include "base64"; base64_encode "Hello!";
