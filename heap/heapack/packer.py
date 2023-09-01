from os import getcwd, chdir, mkdir, walk
from tempfile import gettempdir
from time import time
from os.path import dirname, join
from shutil import copytree
from ..md5 import make_md5_from_file
from json import dump
from tarfile import open as tar_open


class Packer:
    def __init__(self, path: str, output: str):
        self.path = path
        self.name = None
        self.version = [None, None, None]
        self.package = None
        self.author = []
        self.require = []

        self.output = output

    def set_require(self, require: list[str]):
        self.require = require

        return self

    def set_authors(self, authors: list[str]):
        self.author = authors

        return self

    def add_require(self, require: str):
        self.require.append(require)

        return self

    def set_name(self, name: str):
        self.name = name

        return self

    def set_package(self, package: str):
        self.package = package

        return self

    def add_author(self, author: str):
        self.author.append(author)

        return self

    def set_version(self, version: tuple | list):
        self.version = list(version)

        return self

    def cdmkdir(self, path: str):
        mkdir(path)
        chdir(path)

    def pack(self):
        print(f"准备打包:")
        print(f"- Name:{self.name}")
        print(f"- Package Name:{self.package}")
        print(f"- Require:{self.require}")
        print(f"- Author:{self.author}")
        print(f"- Version:{self.version}")

        temp_dir_path = gettempdir()
        old_path = getcwd()
        temp_project_name = f"heap-{time()}"
        md5 = {}

        # 创建一个临时打包目录
        chdir(temp_dir_path)

        print(f" 复制文件...")
        copytree(join(old_path, self.path), join(temp_dir_path, temp_project_name))

        chdir(temp_project_name)

        # 此时已经进入打包的路径, 因此校验求和

        print(f" Md5 计算")
        for root, _, files in walk("."):
            for file in files:
                fpath = join(root, file)  # 获得文件路径
                md5[fpath] = make_md5_from_file(fpath)
        print(f"Md5 Info:")
        for key, v in md5.items():
            print(f"- [{key}] -> {v}")

        # 完成文件求和

        # 保存到project.json

        with open("project.json", "w") as f:
            project = {
                "project": {
                    "name": self.name,
                    "package": self.package,
                    "author": self.author,
                    "version": self.version,
                    "require": self.require,
                },
                "md5": md5,
            }

            dump(project, f)

        # 打包
        print("正在写文件")
        with tar_open(join(old_path, self.output), "w") as tar:
            tar.add(".", arcname="")
        print("完成!")


if __name__ == "__main__":
    p = Packer("../manager", "../1")

    p.set_package("com.heap.test")
    p.pack()
