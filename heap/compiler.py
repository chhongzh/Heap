from .ast import ASTNode
from .common import message
from os import system
from shlex import join


def compile_from_builded_ast(
    ast: list[ASTNode],
    compiler_path: str = "g++",
    compiler_options: list[str] = ["-std=c++14"],
    other_include: list[str] = [],
    binary_path=None,
    include_path_for_heap="heap",
    cpp_path=None,
):
    message("Compiler", "C Heap Compiler V2.0.0")

    c_content = [
        "#include <Heap.hpp>\n",
        *[f"#include <{lib_name}>\n" for lib_name in other_include],
        "\n",
        "int main(){\n",
    ]

    if not cpp_path and not binary_path:
        message("Compiler", "Error: No cpp_path and binary_path, exited!")
        return

    if cpp_path:
        message("Task", 'Current task is "Frontend Job"')
        for stmt in ast:
            c_content.append(stmt.trans_C() + ";")

        c_content.append("return 0;\n}\n")

        with open(cpp_path, "w") as f:
            f.writelines(c_content)

    if binary_path:
        message("Task", 'Current task is "Backend Job"')
        message(
            "Compiler",
            f'Compiler path is "{compiler_path}" and options is {repr(compiler_options)}',
        )

        message("Compiler", "Calling compiler...")
        cmd = join(
            [
                compiler_path,
                "-I",
                include_path_for_heap,
                *compiler_options,
                cpp_path,
                "-o",
                binary_path,
            ]
        )
        message("Compile", f'Cmd is "{cmd}"')
        system(cmd)
    message("Compiler", "All jobs done.")
