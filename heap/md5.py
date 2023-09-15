# Heap - Lang
# chhongzh

from hashlib import md5


def make_md5_from_file(file_path: str):
    m = md5()

    with open(file_path, "rb") as f:
        block = f.read()
        m.update(block)

    return m.hexdigest()
