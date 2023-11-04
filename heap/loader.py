"""一个简单的文件加载器"""


def loader(path: str) -> str:
    """加载一个文件并返回内容"""

    with open(path, encoding="utf-8") as f:
        return f.read()
