from urllib import request


from ..asts import Func, Root


def web_get(father: Root | Func, url: str):
    father.stack.append(request.urlopen(url))
