LIBS = {
    "math": "_math",
    "array": "_arrayutils",
    "type": "_type",
    "system": "_system",
    "random": "_random",
    "terminal":"_terminal",
}
HEAP_LIBS = {
    "functionic": "functionic.heap",
    "endl": "endl.heap",
    "builtin": "builtin.heap",
    "super_header":"super_header",
}

for k,v in LIBS.items():
    if(k == 'builtin'):
        continue

    print(f"include \"{k}\";")

for k,v in HEAP_LIBS.items():
    if(k == 'builtin'):
        continue

    print(f"include \"{k}\";")