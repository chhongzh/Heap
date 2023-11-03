# 构建Heap可执行文件

from subprocess import run
from sys import executable
from shutil import rmtree, copytree
from os import chdir, rename, name

print("准备构建")

rmtree("dist", ignore_errors=True)

run([executable, "-m", "nuitka", "cli.py", "--standalone"])
rename("cli.dist", "dist")

print("复制heap资源文件到目录")
copytree("heap/", "dist/heap/")

print("Copy done")
print(f'Out in "dist-{name}/", bin file in "dist/cli.bin"')

rename("dist", f"dist-{name}")
