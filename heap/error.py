# Heap @ 2023
# chhongzh

"""
Heap中所有的错误类型
"""


class BaseError:
    """
    基础错误类型

    请注意, 在代码中请勿抛出这个错误, 而是Error
    """

    def __init__(self, val: str, pos: int, *args):
        self.args = args
        self.val = val
        self.pos = pos


class Error(BaseError):
    pass


class LexerError(BaseError):
    pass


class ObjError(Error):
    pass


class InputError(Error):
    pass


class NotCloseTag(Error):
    pass


class HeapOverflow(Error):
    pass


class IncludeError(Error):
    pass


class NotDefine(Error):
    pass


class SyntaxErr(Error):
    pass


class CallErr(Error):
    pass


class BuilderErr(Error):
    pass


class PopFromEmptyStack(Error):
    pass


ERRDICT = {
    "BaseError": BaseError,
    "Error": Error,
    "ObjError": ObjError,
    "InputError": InputError,
    "NotCloseTag": NotCloseTag,
    "HeapOverflow": HeapOverflow,
    "IncludeError": IncludeError,
    "NotDefine": NotDefine,
    "SyntaxErr": SyntaxErr,
    "CallError": CallErr,
    "BuilderErr": BuilderErr,
    "PopFromEmptyStack": PopFromEmptyStack,
}
