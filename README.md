# Heap
Heap是一门类似于汇编的编程语言

## Features
- 变量支持
```
> push 1;
> set one $;
> get one;
< 1
```

- 函数支持

```
> func hello:
..    push "Hello world";
..    print;
..endfunc
> hello;
Hello world
```

- 注释支持
  
```
> # 一行注释
>  
```

- 导入支持

```
> # Dir Tree:
> # a:
> # |-a.heap
> # |-b:
> # | |-c.heap
> # main.heap
> 
> # main.heap
> include "a/a.heap";
> 
> # a/a.heap
> include "b/c.heap"

```

## Install
安装Python环境后, 执行`python3 -c "$(curl -fsSL https://raw.githubusercontent.com/chhongzh/Heap/main/installer.py)"`. 安装脚本会自动完成安装.