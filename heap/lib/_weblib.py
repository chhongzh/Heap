# Heap @ 2023
# chhongzh

"""
网络操作模块
"""

from ..asts import Func, Root
from urllib import request
from ..log import info


def web_get(father: Root | Func, url: str) -> None:
    info(f"[Module]: [weblib]: Send req to {url}")
    father.stack.append(request.urlopen(url))


def web_make_req(father: Root | Func, url: str):
    father.stack.append(request.Request(url))


def web_send_req(father: Root | Func, req: request.Request):
    father.stack.append(request.urlopen(req))


def web_req_add_header(father: Root | Func, req: request.Request, key: str, value: str):
    req.add_header(key, value)

    father.stack.append(req)


def web_getcode(father: Root | Func, req: request.Request):
    father.stack.append(req.status)
