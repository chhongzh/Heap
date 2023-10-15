// Heap Stack
// Heap堆栈实现
// chhongzh

#ifndef __HEAP_STACK_HPP
#define __HEAP_STACK_HPP
#endif

#ifndef __HEAP_OBJECT_HPP
#include "HeapObject.hpp"
#endif

class HeapStack
{
public:
    std::vector<HeapObject *> stack;

    void push(HeapObject *object);
    HeapObject *pop();

    void clear();
};

void HeapStack::push(HeapObject *object)
{
    HeapStack::stack.push_back(object);
}

HeapObject *HeapStack::pop()
{
    HeapObject *value = HeapStack::stack.back();
    HeapStack::stack.pop_back();

    return value;
}