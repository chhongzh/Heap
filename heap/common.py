from os import get_terminal_size


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


def go_C(obj):
    if isinstance(obj, str):
        return '"' + obj.replace('"', '\\"') + '"'
    else:
        return repr(obj)


def message(name, msg: str):
    width = get_terminal_size()[0]
    left = f"[{name}]"
    right = msg
    space_cnt = width - (len(left) + len(right))
    if space_cnt >= 0:
        print(f'{right}{" "*space_cnt}{left}')
    else:
        print(f"{right[:space_cnt-3]}...{left}")
