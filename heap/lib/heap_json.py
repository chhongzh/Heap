# Heap
# chhongzh @ 2023

import json
from ..asts import Root, Func


def from_json(father: Func | Root, raw_json_string: str):
    father.stack.append(json.loads(raw_json_string))


def to_json(father: Func | Root, heap_object):
    father.stack.append(json.dumps(heap_object, ensure_ascii=False))


HEAP_EXPORT_FUNC = {
    "json_load": from_json,
    "json_dump": to_json,
}
