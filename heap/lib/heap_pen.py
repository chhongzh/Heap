from turtle import Pen
from ..asts import Func, Root


def pen(_: Root):
    t = Pen()

    t.screen.title("Heap Pen (Base on python turtle.)")
    return t


def pen_forward(_: Root, pen: Pen, distance):
    pen.forward(distance)

    return pen


def pen_left(_: Root, pen: Pen, angle):
    pen.left(angle)
    return pen


def pen_right(_: Root, pen: Pen, angle):
    pen.right(angle)
    return pen


def pen_textinput(_: Root | Func, pen: Pen, title: str, prompt: str):
    pen.screen.textinput(title, prompt)


def pen_done(_: Root, pen: Pen):
    pen.screen.mainloop()


HEAP_EXPORT_FUNC = {
    "pen": pen,
    "pen_left": pen_left,
    "pen_right": pen_right,
    "pen_done": pen_done,
    "pen_forward": pen_forward,
}
