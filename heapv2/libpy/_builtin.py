def println(runner, ctx: dict, *args):
    print(*args, sep="")


def readln(runner, ctx: dict, prompt):
    return input(prompt)
