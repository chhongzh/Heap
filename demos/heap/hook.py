from .eprint import print_error


def _print(val):
    print(val, end="")


def _raise_error(error):
    print_error(error)

    exit(1)
