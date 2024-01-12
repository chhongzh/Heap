# chhongzh @ 2023
# Heap - 标准库 - Queue(队列)

"""
Queue队列
"""
from queue import Queue
from ..asts import Root


def queue_queue(_: Root):
    return Queue()


def queue_put(_: Root, q: Queue, anything):
    q.put(anything)
    return q


def queue_get(_: Root, q: Queue):
    return q.get()


def queue_empty(_: Root, q: Queue) -> bool:
    return q.empty()


def queue_full(_: Root, q: Queue) -> bool:
    return q.full()


def queue_qsize(_: Root, q: Queue) -> bool:
    return q.qsize()


HEAP_EXPORT_FUNC = {
    "queue_empty": queue_empty,
    "queue_full": queue_full,
    "queue_get": queue_get,
    "queue_put": queue_put,
    "queue_qsize": queue_qsize,
    "queue_queue": queue_queue,
}
