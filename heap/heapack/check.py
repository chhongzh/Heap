def check_package_name(package_name: str):
    # xx.xxx.xx
    not_allow = list(" ")
    allow = list("abcdefghijklmnopqrstuvwxyzABCDEFGIHJLMNOPQRSTUVWXYZ.1234567890")

    for char in package_name:
        if char in not_allow or char not in allow:
            return False
    else:
        return True


def check_version(version: str):
    allow = list("1234567890.")

    for char in version:
        if char not in allow:
            return False
    else:
        return True
