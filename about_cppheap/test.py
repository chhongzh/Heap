from heap.cppheap.emitter import Emitter
from heap.asts import Root
from heap import Lexer, Builder

body = """
push "Hello World!"; # string
print;
"""

l = Lexer(body)
lex = l.lex()

b = Builder(lex)
r = b.parse()


e = Emitter(r)

a = e.emit()

with open("t.cpp", "w") as f:
    f.writelines(a)
