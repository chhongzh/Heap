from dataclasses import dataclass


@dataclass
class MetaInfo:
    start_pos: int
    end_pos: int


class Token:
    def __init__(self, type: int, value, meta: MetaInfo):
        self.type = type
        self.value = value
        self.meta = meta

    def __repr__(self) -> str:
        return f"Token(type={repr(self.type)},value={repr(self.value)},meta={repr(self.meta)})"
