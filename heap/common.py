def reader(fpath: str):
    with open(fpath) as f:
        return f.read()


class Evalable:
    def eval(self, runner, context: dict): ...


def get_type(obj):
    if isinstance(obj, int):
        return "int"
    elif isinstance(obj, str):
        return "string"
    elif isinstance(obj, bool):
        return "bool"
    elif isinstance(obj, float):
        return "float"
    elif obj == None:
        return None
    return obj.__class__.__name__
