#include <string>
#include <sstream>

#ifndef __HEAP_TO_STRING_HPP
#define __HEAP_TO_STRING_HPP
#endif

std::string heap_object_to_string(HeapObject *obj)
{
    std::ostringstream a;
    int type = obj->get_type();
    if (type == INT)
    {
        return std::to_string(std::any_cast<int>(obj->get_value()));
    }
    else if (type == STR)
    {
        return std::any_cast<std::string>(obj->get_value());
    }
    else if (type == FLOAT)
    {
        return std::to_string(std::any_cast<double>(obj->get_value()));
    }
    else
    {
        throw "Unkown Value!";
    }
}