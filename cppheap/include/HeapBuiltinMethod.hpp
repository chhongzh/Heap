// Heap Builtin Method

void __print(HeapStack *stack)
{
    std::string val = heap_object_to_string(stack->pop());

    std::cout << val;
}