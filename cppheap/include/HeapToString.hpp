#include <string>
std::string heap_object_to_string(HeapObject obj)
{
    int type = obj.get_type();
    if (type == INT)
    {
        return std::to_string(std::any_cast<int>(obj.get_value()));
    }
    else if (type == STR)
    {
        return std::any_cast<std::string>(obj.get_value());
    }
    else if (type == FLOAT)
    {
        return std::to_string(std::any_cast<float>(obj.get_value()));
    }
    else
    {
        throw "Unkown Value!";
    }
}