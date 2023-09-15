from .error import BaseError


def print_error(error: BaseError):
    print(
        f"""Encountered an error -> {error.__class__.__name__} -> Token:{error.val}, Pos:{error.pos}, {error.args};"""
    )
