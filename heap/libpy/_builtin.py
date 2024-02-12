def println(runner, ctx, *args):
    print(*args, sep="")


def readln(runner, ctx, prompt):
    return input(prompt)


def pow(runner, ctx, a, b):
    return a**b
