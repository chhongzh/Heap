# chhongzh @ 2023
# 类型转换

from ..asts import Root, Func


# 转字符串
def to_str(father: Root | Func):
    father.stack[-1] = str(father.stack[-1])


# 转数字
def to_int(father: Root | Func):
    father.stack[-1] = int(father.stack[-1])


# 转小数
def to_float(father: Root | Func):
    father.stack[-1] = float(father.stack[-1])
