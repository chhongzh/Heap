from os import chdir, mkdir, rename, walk
from os.path import exists, join
from json import load, dump
from tarfile import open as tar_open
from time import time
from ..md5 import make_md5_from_file
from shutil import copytree, rmtree


class Unpacker:
    def __init__(self, project_path: str, file_path: str):
        self.project_path = project_path
        self.file_path = file_path

    def trymkcd(self, path):
        if not exists(path):
            mkdir(path)

        chdir(path)

    def install(self):
        project_data_path = join(self.project_path, "project.json")
        project_data = None
        temp_dir = f"heap-{time()}"
        file_md5 = {}
        haserr = False
        # Check the project file.
        if not exists(project_data_path):
            print("安装失败: Project Data不存在.")

        if not exists(self.file_path):
            print("安装失败: 安装文件不存在")

        with open(project_data_path) as f:
            project_data = load(f)

        with tar_open(self.file_path) as f:
            f.extractall(temp_dir)

        # 读取安装包
        # chdir(join(self.project_path,'lib'))
        chdir(temp_dir)

        with open("project.json") as f:
            heapack = load(f)

        # 查照依赖:
        not_install = set(heapack["project"]["require"]) & set(project_data["require"])

        if not_install:
            print(f"注意!以下heapack未处理, 请先安装它们{not_install}")
            return

        print("准备安装:")
        print(f"- Name:{heapack['project']['name']}")
        print(f"- Package Name:{heapack['project']['package']}")
        print(f"- Require:{heapack['project']['require']}")
        print(f"- Author:{heapack['project']['author']}")
        print(f"- Version:{heapack['project']['version']}")

        # Check md5
        # 先计算一下解压的文件的MD5

        for root, _, files in walk("."):
            for file in files:
                fpath = join(root, file)
                file_md5[fpath] = make_md5_from_file(fpath)

        print("验证Md5:")
        for key, v in heapack["md5"].items():
            if key == join(".", "project.json"):
                continue
            data = file_md5.get(key, None)

            if data is None:
                # 左边是记录 右边是当前
                print(f"- [{key}]({v[:4]}...{v[-4:]}) != [{key}](Not found.)")

            elif data != v:
                print(f"- [{key}]({v[:4]}...{v[-4:]}) != [{key}]({v[:4]}...{v[-4:]})")

                # raise Exception(data, v, data == v)

            elif data == v:
                print(f"- [{key}]({v[:4]}...{v[-4:]}) == [{key}]({v[:4]}...{v[-4:]})")
        # 判断是否有错误
        if haserr:
            print("注意: 此安装包与记录的不符可能被篡改")
            return

        print("- 全部通过")

        # 添加到项目的requires
        chdir("..")

        project_data["require"].append(heapack["project"]["package"])
        # 写入文件
        with open("project.json", "w") as f:
            dump(project_data, f, ensure_ascii=False)

        # Copy File to Lib:

        self.trymkcd("lib")

        print("复制到Lib...")
        copytree(join("..", temp_dir), heapack["project"]["package"])

        print("删除临时目录")
        rmtree(join("..", temp_dir))

        print("Done!")
