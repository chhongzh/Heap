import subprocess
import sys
import os
import uuid
import zipfile


def ask(prompt: str, value=True):
    prompt = input(f'{prompt} ({"Y" if value else "y"}/{"n" if value else "N"})')
    if prompt.lower() == "y":
        return True
    elif prompt.lower() == "n":
        return False
    else:
        return value


def install_module(name: str):
    subprocess.call(
        [sys.executable, "-m", "pip", "install", name], stdout=subprocess.PIPE
    )


print("安装Heap")

if (3, 9, 6) > (sys.version_info.major, sys.version_info.minor, sys.version_info.micro):
    print(
        f"你的python版本太低了, 尝试升级. (需要Python3.9.6或更高, 而不是:Python{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})"
    )

try:
    import rich, prompt_toolkit, requests
except ImportError:
    print("缺少依赖, 补全.")
    print("下载并安装rich")
    install_module("rich")
    print("安装成功")
    print("下载并安装prompt_toolkit")
    install_module("prompt_toolkit")
    print("安装成功")
    print("下载并安装requests")
    install_module("requests")
    print("安装成功")
    print("下载并安装click")
    install_module("click")
    print("安装成功")

    import rich, prompt_toolkit, requests


path = os.getcwd()
path = prompt_toolkit.shortcuts.input_dialog("警告", "将会安装在:", default=path).run()
print(f'安装在:"{path}"')

if not path:
    print("取消安装")
    exit(0)

if not os.path.exists(path):
    print("错误: 不合法的路径")
    exit(1)

os.chdir(path)

version = None

print("尝试请求版本列表")
try:
    req = requests.get("https://api.github.com/repos/chhongzh/heap/releases", timeout=3)
except TimeoutError:
    print("尝试请求Github时出现错误, Github不可用.")
    print("尝试使用gitee手动下载")
    prompt_toolkit.shortcuts.message_dialog(
        "错误", "尝试获取版本信息时, 遇到了TimeoutError. 无法获得版本数据."
    )

    exit(1)

version_name = [obj["tag_name"] for obj in req.json()]
print(f"共有{len(version_name)}个版本")


version_object = prompt_toolkit.shortcuts.radiolist_dialog(
    "选择", "选择版本以安装", values=list(zip(req.json(), version_name))
).run()

url_path = version_object["zipball_url"]
fname = str(uuid.uuid4())

print(f"下载地址为:{url_path}")
print(f"本地文件地址为:{fname}")

req = requests.get(url_path, stream=True)
with open(fname, "wb") as file:
    for chunck in req.iter_content(chunk_size=512):
        file.write(chunck)

print("下载成功")

with zipfile.ZipFile(f"{fname}") as z:
    for file in z.namelist():
        print(f"解压:{file}")
        z.extract(file, ".")

os.remove(fname)
print(f"删除文件:{fname}")

print()
print("安装完成!")
print()

print("输入`python3 cli.py`启动Heap")
