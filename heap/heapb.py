# Heap @ 2024
# chhongzh

"""
heapb - Heap Bytes.
存储ast树
"""

from .asts import Root
from pickle import dump, load


def writer(root: Root, path: str):
    with open(path, "wb") as f:
        dump(root, f)


def loader(path: str) -> Root:
    with open(path, "rb") as f:
        return load(f)
