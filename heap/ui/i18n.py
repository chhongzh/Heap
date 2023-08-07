import json
import os.path


class i18n:
    def __init__(self, file_path, default) -> None:
        p = file_path
        if not os.path.exists(file_path):
            p = default
        with open(p) as f:
            self.d = json.load(f)

    def t(self, key: str):
        temp = self.d

        for item in key.split("."):
            temp = temp[item]

        return temp