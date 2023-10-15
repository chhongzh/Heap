from ..asts import Func, Input, Print, Push, Root


class Emitter:
    def __init__(self, root: Root):
        self.__root = root
        self.__var_iter = 0
        self.__file = []
        self.__indent = 0

        self.__message("Begin to emit.")

    def __message(self, str: str):
        print(f"cppheap: {str}")

    def __emit_one(self, node: Push):
        if isinstance(node, Push):
            self.__message("Emit Push block.")
            self.__make_push(node.val)
        elif isinstance(node, Print):
            self.__message("Emit Print block.")
            self.__emit_print()
        elif isinstance(node, Input):
            self.__message("Emit Input block.")
            self.__emit_input()
        elif isinstance(node, Func):
            self.__message("Emit Func block.")
            self.__emit_func(node)

    def __emit_input(self):
        self.__new_cpp_line("__input(stack);")

    def __emit_func(self, node: Func):
        func_name = f"heap_user_func_{node.name}"
        args_dec_statement = []
        for arg in node.args:
            args_dec_statement.append(f"HeapObject *const_var_{arg}")

        self.__message(
            f'Make func. name:"{func_name}", with args "{", ".join(args_dec_statement)}"'
        )

        self.__new_cpp_line(
            f"auto {func_name} = [stack]({', '.join(args_dec_statement)})"
        )
        self.new_block()

        self.__emit_list(node.body)

        self.end_block("};")

    def __emit_list(self, lst: list):
        for i in lst:
            self.__emit_one(i)

    def __new_cpp_line(self, line: str):
        unendl = "\\n"
        endl = "\n"
        self.__file.append(f"{' '*self.__indent}{line.replace(endl,unendl)}\n")

        # Python3.11神奇的特性, 必须这么写. 模版字符串不支持转译!!!

    def __new_const(self, r_value: int | float | str) -> str:
        type = self.__get_type(r_value)
        self.__new_cpp_line(
            f"HeapObject const_value_{self.__var_iter} = HeapObject({type},{self.__make_cpp_obj(r_value)});"
        )
        self.__var_iter += 1

        return f"const_value_{self.__var_iter-1}"

    def __get_type(self, r_value: int | float | str):
        if isinstance(r_value, str):
            return "3"
        elif isinstance(r_value, int):
            return "1"
        elif isinstance(r_value, float):
            return "2"

    def __emit_print(self):
        self.__new_cpp_line("__print(stack);")

    def __make_cpp_obj(self, value: int | float | str):
        if isinstance(value, str):
            return f'std::string("{value}")'
        elif isinstance(value, int):
            return value
        elif isinstance(value, float):
            return value

    def __make_push(self, r_value: int | float | str):
        # 申请一个常量, 然后推入object
        id = self.__new_const(r_value)

        self.__new_cpp_line(f"stack->push(&{id});")
        self.__message(f"stack->push(&{id});")

    def new_block(self, op="{"):
        self.__new_cpp_line(op)
        self.__indent += 4

    def end_block(self, op="}"):
        self.__indent -= 4
        self.__new_cpp_line(op)

    def emit(self):
        self.__new_cpp_line("// CppHeap project")
        self.__new_cpp_line("")
        self.__new_cpp_line('#include "Heap.hpp"')
        self.__new_cpp_line("")
        self.__new_cpp_line("int main()")
        self.new_block()

        # Main function
        self.__new_cpp_line("// For Stack")
        self.__new_cpp_line("HeapStack t_stack = HeapStack();")
        self.__new_cpp_line("HeapStack *stack = &t_stack;")
        self.__new_cpp_line("")

        self.__emit_list(self.__root.body)

        self.__new_cpp_line("return 0;")

        self.end_block()

        return self.__file
