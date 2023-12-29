from os import get_terminal_size
from os.path import exists, join
from shlex import split

import click

from heap import Lexer, Builder, Runner

out = lambda *args, **kwargs: print(*args, **{**kwargs, "end": ""})
X, Y = 0, 0


class Crack_Runner(Runner):
    def CrAcK(self):
        # The main debug thread is on here.

        self.CrAcK_oldvisit = self.visit
        self.CrAcK_oldrun = self.run

        def CrAcK_visit(node, father):
            FLAG = True

            if self.Crack_shutupcnt > 0:
                self.Crack_shutupcnt -= 1
                Ui.good_message(f"Shutuptting, {self.Crack_shutupcnt}")
                return self.CrAcK_oldvisit(node, father)

            while FLAG:
                Ui.write_title()
                Ui.next_line()
                Ui.good_message(f"Status:")
                Ui.next_line()
                Ui.good_message(f'  File Path="{self.CrAcK_filepath}"')
                Ui.next_line()
                Ui.good_message(f'  Tokens cnt="{self.CrAcK_tokscnt}"')
                Ui.next_line()
                Ui.good_message(f'  Level="{"/".join(self.running_block)}"')
                Ui.next_line()
                Ui.good_message(f'  Current="{node.__class__.__name__}"')
                Ui.next_line()
                Ui.good_message(f'  Stack (Last three items)="{father.stack[-3:]}"')
                Ui.next_line()

                command = split(Ui.query_command(":"))

                if len(command) == 0:
                    FLAG = False
                elif len(command) == 1:
                    if command[0] in ("next", "n"):
                        Ui.good_message(f'Execute="{node.__class__.__name__}"')
                        FLAG = False

                    elif command[0] in ("level",):
                        Ui.good_message(f'  Level="{"/".join(self.running_block)}"')

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
                        Ui.good_message(f"  Going shutup, blocks={command[1]}")
                        self.Crack_shutupcnt = int(command[1])
                        FLAG = False

            return self.CrAcK_oldvisit(node, father)

        def CrAcK_run():
            self.CrAcK_oldrun()

            Ui.good_message("Done !")

        self.visit = CrAcK_visit
        self.run = CrAcK_run

        pass


class Ui:
    def main_loop(file_path: str):
        out(Cursor.clear())

        # Before debug
        with open(file_path) as f:
            CONTENT = f.read()
        l = Lexer(CONTENT)
        toks = l.lex()

        b = Builder(toks, file_path)
        ast_tree = b.parse()

        r = Crack_Runner(ast_tree, join(__file__, "heap"))
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
