# Heap UI. 多行输入实现
# chhongzh @ 2023


def multiline_input(end="'") -> list:
    buffer = []

    while True:
        line = input("... ")
        if line == end:
            break
        buffer.append(line)

    return buffer


if __name__ == "__main__":
    multiline_input()
