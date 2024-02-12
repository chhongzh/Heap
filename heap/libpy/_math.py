import math


def sqrt(runner, ctx: dict, num):
    return math.sqrt(num)


def pow(runner, ctx: dict, num):
    return math.pow(num)


def acos(runner, ctx: dict, num):
    return math.acos(num)


def acosh(runner, ctx: dict, num):
    return math.acosh(num)


def asin(runner, ctx: dict, num):
    return math.asin(num)


def asinh(runner, ctx: dict, num):
    return math.asinh(num)


def atan(runner, ctx: dict, num):
    return math.atan(num)


def atan2(runner, ctx: dict, num):
    return math.atan2(num)


def atanh(runner, ctx: dict, num):
    return math.atanh(num)


def ceil(runner, ctx: dict, num):
    return math.ceil(num)


def comb(runner, ctx: dict, num, num1):
    return math.comb(num, num1)


def copysign(runner, ctx: dict, num, num1):
    return math.copysign(num, num1)


def cos(runner, ctx: dict, num):
    return math.cos(num)


def cosh(runner, ctx: dict, num):
    return math.cosh(num)


def degrees(runner, ctx: dict, num):
    return math.degrees(num)


def dist(runner, ctx: dict, num, num1):
    return math.dist(num, num1)


def erf(runner, ctx: dict, num):
    return math.erf(num)


def erfc(runner, ctx: dict, num):
    return math.erfc(num)


def exp(runner, ctx: dict, num):
    return math.exp(num)


def exp2(runner, ctx: dict, num):
    return math.exp2(num)


def expm1(runner, ctx: dict, num):
    return math.expm1(num)


def fabs(runner, ctx: dict, num):
    return math.fabs(num)


def factorial(runner, ctx: dict, num):
    return math.factorial(num)


def floor(runner, ctx: dict, num):
    return math.floor(num)


def fmod(runner, ctx: dict, num, num1):
    return math.fmod(num, num1)


def frexp(runner, ctx: dict, num):
    return math.frexp(num)


def fsum(runner, ctx: dict, num):
    return math.fsum(num)


def gamma(runner, ctx: dict, num):
    return math.gamma(num)


def gcd(runner, ctx: dict, *num):
    return math.gcd(*num)


def hypot(runner, ctx: dict, *num):
    return math.hypot(*num)


def isqrt(runner, ctx: dict, num):
    return math.isqrt(num)
