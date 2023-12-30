# 构建Heap可执行文件

from subprocess import run
from sys import executable
from shutil import rmtree, copytree, make_archive
from os import chdir, rename
from platform import system, machine
from heap.version_info import HEAP_VERSION_STR
from time import strftime
from os.path import split
from datetime import datetime

build_time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

compile_info = f"""# This file may auto genrated by builder.

IS_COMPILE = True
COMPILE_DATE = '{build_time}'
"""

chdir(split(__file__)[0])

print("准备构建Heap")
print(f"版本:{HEAP_VERSION_STR}")

print("生成版本信息:")
with open("heap/compile_info.py", "w") as f:
    f.write(compile_info)

rmtree("dist", ignore_errors=True)
rmtree(f"heap-{HEAP_VERSION_STR}-{system()}-{machine()}", ignore_errors=True)

run([executable, "-m", "nuitka", "cli.py", "--standalone"])
rename("cli.dist", "dist")

print("复制heap资源文件到目录")
copytree("heap/", "dist/heap/")

print("复制完成")

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

compile_info = f"""# This file may auto genrated by builder.

IS_COMPILE = False
COMPILE_DATE = '{build_time}'
"""

chdir(split(__file__)[0])

with open("heap/compile_info.py", "w") as f:
    f.write(compile_info)
