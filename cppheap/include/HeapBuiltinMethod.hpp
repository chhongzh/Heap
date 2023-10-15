// Heap Builtin Method

#ifndef __HEAP_BUILT_IN_METHOD_HPP
#define __HEAP_BUILT_IN_METHOD_HPP
#endif

void __print(HeapStack *stack)
{
    std::string val = heap_object_to_string(stack->pop());

    std::cout << val;
}

void __input(HeapStack *stack)
{
    std::string val;

    std::cin >> val;

    HeapObject obj = HeapObject(STR, val);
    stack->push(&obj);
}