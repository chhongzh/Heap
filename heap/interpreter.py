# Heap @ 2023
# chhongzh

"""给repr用的东西"""


def _print(val, store: list) -> None:
    "存储输出到缓存"
    store.append(val)
