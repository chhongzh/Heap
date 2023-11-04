# Heap @ 2023
# chhongzh

"""
Heap中的Token数据结构
"""


from dataclasses import dataclass


@dataclass
class MetaInfo:
    start_pos: int
    end_pos: int


class Token:
    def __init__(self, token_type: int, token_value, meta: MetaInfo):
        self.type = token_type
        self.value = token_value
        self.meta = meta

    def __repr__(self) -> str:
        return f"Token(type={repr(self.type)},value={repr(self.value)},meta={repr(self.meta)})"
