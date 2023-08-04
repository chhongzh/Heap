class BaseError:
    def __init__(self, val: str, pos: int, *args):
        self.args = args
        self.val = val
        self.pos = pos


class Error(BaseError):
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


ERRDICT = {
    "BaseError": BaseError,
    "Error": Error,
    "ObjError": ObjError,
    "InputError": InputError,
    "NotCloseTag": NotCloseTag,
    "HeapOverflow": HeapOverflow,
    "IncludeError": IncludeError,
}
