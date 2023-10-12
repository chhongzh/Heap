#include "include/Heap.hpp"

using namespace std;

int main(int argc, char *argv[])
{
    // Begin Value Scope
    HeapStack stack = HeapStack();
    HeapObject const_var_1 = HeapObject(3, std::string("string"));
    stack.push(const_var_1);

    // Begin Main
    __print(&stack);

    std::cout << std::endl;

    std::cout << stack.stack.size();
}
