from inspect import isfunction
from os import get_terminal_size
from os.path import split as osplit
from shlex import split

import click

from heap import Lexer, Builder, Runner
from heap.asts import Func
from heap import hook
from textwrap import shorten

out = lambda *args, **kwargs: print("".join(args), **{**kwargs, "end": ""})
X, Y = 0, 0


class Crack_Runner(Runner):
    def CrAcK(self):
        # The main debug thread is on here.

        self.CrAcK_oldvisit = self.visit
        self.CrAcK_oldrun = self.run

        def CrAcK_print(val):
            Ui.print(val)

        def CrAcK_visit(node, father):
            FLAG = True

            if self.Crack_shutupcnt > 0:
                self.Crack_shutupcnt -= 1
                return self.CrAcK_oldvisit(node, father)

            while FLAG:
                Ui.write_title()
                Ui.next_line()
                Ui.good_message(f"Status:")
                Ui.next_line()
                Ui.good_message(f'  Level="{"/".join(self.running_block)}"')
                Ui.next_line()
                Ui.good_message(f'  Current="{node.__class__.__name__}"')
                Ui.next_line()
                Ui.good_message(f'  Stack (Last three items)="{father.stack[-3:]}"')
                Ui.next_line()
                Ui.good_message(f"-" * (get_terminal_size()[0] - 2))
                Ui.next_line()

                command = split(Ui.query_command(":"))

                if len(command) == 0:
                    FLAG = False
                elif len(command) == 1:
                    if command[0] in ("next", "n"):
                        Ui.good_message(f'Execute="{node.__class__.__name__}"')
                        FLAG = False

                    elif command[0] in ("level",):
                        Ui.good_message(f'Level="{"/".join(self.running_block)}"')

                    elif command[0] in ("vars",):
                        Ui.good_message(f"All vars:")
                        for name, type in father.var_ctx.items():
                            if not (isfunction(type) or isinstance(type, Func)):
                                Ui.good_message(f"  {name}={type}")
                    elif command[0] in ("inspect", "i"):
                        variable_cnt = 0
                        func_cnt = 0
                        for type in father.var_ctx.values():
                            if isfunction(type) or isinstance(type, Func):
                                func_cnt += 1
                            else:
                                variable_cnt += 1
                        Ui.good_message(f"Inspect")
                        Ui.good_message(f"  Variables cnt={variable_cnt}")
                        Ui.good_message(f"  Funcs cnt={func_cnt}")

                    elif command[0] in ("status",):
                        Ui.good_message(f"Status:")
                        Ui.good_message(f'  File Path="{self.CrAcK_filepath}"')
                        Ui.good_message(f'  Tokens cnt="{self.CrAcK_tokscnt}"')
                        Ui.good_message(f'  Level="{"/".join(self.running_block)}"')
                        Ui.good_message(f'  Current="{node.__class__.__name__}"')
                        Ui.good_message(
                            f'  Stack (Last three items)="{father.stack[-3:]}"'
                        )

                    elif command[0] in ("exit", "quit"):
                        exit(0)
                elif len(command) == 2:
                    if command[0] in ("shutup", "s"):
                        Ui.good_message(f"Going shutup, blocks={command[1]}")
                        self.Crack_shutupcnt = int(command[1])
                        FLAG = False

            return self.CrAcK_oldvisit(node, father)

        def CrAcK_run():
            self.CrAcK_oldrun()

            Ui.good_message("Done !")

        self.visit = CrAcK_visit
        self.run = CrAcK_run
        hook.print_val = CrAcK_print

        pass


class Ui:
    def print(j):
        Cursor.clear_current_line()

        out(f"P|{j}\n")

    def main_loop(file_path: str):
        out(Cursor.clear())

        # Before debug
        with open(file_path, encoding="utf-8") as f:
            CONTENT = f.read()
        l = Lexer(CONTENT)
        toks = l.lex()

        b = Builder(toks, file_path)
        ast_tree = b.parse()

        r = Crack_Runner(ast_tree, osplit(file_path)[0])
        r.CrAcK_filepath = file_path
        r.CrAcK_tokscnt = len(toks)
        r.Crack_shutupcnt = 0
        r.CrAcK()
        r.run()

    def cmd_not_found():
        Ui.bad_message("Command not found.")

    def bad_message(msg: str):
        Cursor.clear_current_line()

        out(f"E|{msg}\n")

    def good_message(msg: str):
        Cursor.clear_current_line()
        out(f"I|{msg}\n")

    def write_title():
        Cursor.go_right_top()
        Cursor.clear_current_line()
        out("HDT - Heap debug tools")

    def next_line():
        global Y, X
        Y += 1
        X = 1

        Cursor.move_to(Y, X)

    def up_line():
        global Y, X
        Y -= 1
        X = 1

        Cursor.move_to(Y, X)

    def query_command(query: str, move_back: bool = True):
        if move_back:
            Cursor.go_right_bottom()
            return input(query)


class Cursor:
    save_pos = lambda: "\033[s"
    restore_pos = lambda: "\033[u"
    clear = lambda: "\033[2J"

    def move_to(l, c):
        global Y, X
        Y = l
        X = c
        out(f"\033[{Y};{X}H")

    def clear_current_line():
        global Y, X
        Cursor.move_to(Y, 1)
        out(" " * (get_terminal_size()[0] - 1), end="")
        Cursor.move_to(Y, X)

    def go_right_bottom():
        global Y, X

        Y = get_terminal_size()[0] - 1
        X = 1
        Cursor.move_to(Y, X)

    def go_next_line():
        global X, Y

        Y += 1
        X = 1
        Cursor.move_to(Y, X)

    def go_right_top():
        global X, Y

        Y = 1
        X = 1
        Cursor.move_to(Y, X)


@click.command("")
@click.argument("filepath")
def __wrapper(filepath):
    Ui.main_loop(filepath)


__wrapper()
