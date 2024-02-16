/* Heap Lang V2.0.0
 * The header of C Heap.
 *
 * Chhongzh @ 2024
 *
 */
#ifndef HEAP_HEADER
#define HEAP_HEADER

#include <cstdarg>
#include <iostream>
#include <string>
#include <math.h>
#include <cstdio>
// 对于类型转换

const auto True = true;
const auto False = false;

// 默认返回值
const auto main_ret = 0;

// 类型别名
using Int = long long;
using String = std::string;
using Bool = bool;
using Void = void;
using Float = double;

// 内置函数
auto println() -> Void
{
    std::cout << std::endl;
}

template <typename T, typename... Ts>
auto println(T current, Ts... left) -> Void
{ // 每一步都会自动展开
    std::cout << current;
    println(left...);
}

template <typename T>
auto readln(T prompt) -> String
{
    String __temp;
    std::cout << prompt;
    std::getline(std::cin, __temp);
    return __temp;
}

auto to_int(String str) -> Int
{
    return std::stol(str);
}

template <typename T>
auto to_str(T val) -> String
{
    return std::to_string(val);
}

auto to_float(String val) -> Float
{
    return std::stod(val);
}
#endif