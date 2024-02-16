from .grammar import File, BinExpr, Statement


def lex(content: str):
    return File.parse_string(content)
