# 构建Heap可执行文件

from subprocess import run
from sys import executable
from shutil import rmtree, copytree, make_archive
from os import chdir, rename
from platform import system, machine
from heap.version_info import HEAP_VERSION_STR


print("准备构建")

rmtree("dist", ignore_errors=True)
rmtree(f"heap-{HEAP_VERSION_STR}-{system()}-{machine()}", ignore_errors=True)

run([executable, "-m", "nuitka", "cli.py", "--standalone"])
rename("cli.dist", "dist")

print("复制heap资源文件到目录")
copytree("heap/", "dist/heap/")

print("Copy done")

chdir("dist")

try:
    rename("cli.exe", "heap.exe")
except:
    rename("cli.bin", "heap.bin")

chdir("../")

make_archive(
    f"dist-{HEAP_VERSION_STR}-{system()}-{machine()}",
    "zip",
    f"dist",
)

rmtree(f"dist")

print(
    f'Out in "heap-{HEAP_VERSION_STR}-{system()}-{machine()}.zip", bin file in "dist/cli.bin"'
)
