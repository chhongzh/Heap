# 构建Heap可执行文件

from subprocess import run
from sys import executable
from shutil import rmtree, copytree
from os import chdir, rename

print("Try to build.")

rmtree("dist", ignore_errors=True)

run([executable, "-m", "nuitka", "cli.py", "--standalone"])
rename("cli.dist", "dist")

print("复制heap资源文件到目录")
copytree("heap/", "dist/heap/")

print("Copy done")
print('Out in "dist/", bin file in "dist/cli.bin"')
