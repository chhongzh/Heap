from heap import Lexer, Builder
from heap.compiler.compile import Compiler

l = Lexer(
    """
#在这个符号内的都是注释!

push "列表支持!";           #完全支持列表
print;                     #打印堆顶的内容

push 1;                    #整数
push "字符串";              #字符串
push -0.1;                 #负数, 小数

push [11,45,14];           #列表

include "utils.heap";      #导入自定义库

print;                     #打印
endl;                      #换行


func hi name:              #定义一个叫做hi的函数并有参数name
    push "Hi, ";
    print;
    get name;              #获得参数name到堆中
    print;
    endl;                  #调用换行函数,支持函数内调用函数
endfunc                    #结束函数定义

input "你叫什么?";          #input函数获得输入, 存放到堆顶

hi $;                      # $符号表示堆顶的数据

"""
)

lex = l.lex()

b = Builder(lex)
root = b.parase()

t = Compiler(root)

va = t.compile()

with open("sb.py", "w") as f:
    f.writelines(va)
