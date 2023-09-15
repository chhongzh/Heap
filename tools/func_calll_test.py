# 生成512个函数并递归调用

content = []

a = list("abcdefghijklmnopqrstuvw")
b = list("abcdefghIjklmnopqrstuvw")
last = 'push "OK"; print'

for i in b:
    for j in a:
        content.append(f"func {i}{j} : {last}; endfunc \n")
        last = f"{i}{j}"


content.append(f"{last};")

with open("dist.txt", "w") as f:
    f.writelines(content)
