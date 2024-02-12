from .grammar import File, BinExpr


def lex(content: str):
    return File.parse_string(content)
