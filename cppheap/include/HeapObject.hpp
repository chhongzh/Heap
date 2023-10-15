// Heap对象实现
// Chhongzh

#ifndef __HEAP_OBJECT_HPP
#define __HEAP_OBJECT_HPP
#endif

class HeapObject
{
public:
    // 1:INT 2:FLOAT 3:STR
    int type;
    std::any value;

    void set_type(int type);
    int get_type();
    void set_value(std::any value);
    std::any get_value();

    HeapObject(int type, std::any raw);
};

HeapObject::HeapObject(int type, std::any raw)
{
    HeapObject::type = type;
    HeapObject::value = raw;
}
void HeapObject::set_type(int type)
{
    HeapObject::type = type;
}
int HeapObject::get_type()
{
    return HeapObject::type;
}

void HeapObject::set_value(std::any value)
{
    if (value.type() == typeid(int))
    {
        return;
    }
    else
    {
        throw "Unkown type";
    }
}

std::any HeapObject::get_value()
{
    return HeapObject::value;
}