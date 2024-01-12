# Heap
Heap是一门指令式编程语言

## Features
- 变量支持
```
> push 1;
> set one $;
> get one;
< 1

> # In the new version, you can do this.
> two = 2;
> get two;
< 2;
```

- 函数支持

```
> func hello:
..    println "Hello World!";
..endfunc
> hello;
Hello world!
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
下载Releases

## Docs
[On this Repo](docs/README.md)

[On github.io](https://chhongzh.github.io#/docs/README)

## Repobeats
![Alt]( https://repobeats.axiom.co/api/embed/9f84794cea3ab96b05702f6a23f1bcfb84164b48.svg)

## PyLint
```
pylint cli.py heap --disable=R0903,C0115,R0911,W0602,R0912,R1710

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 9.99/10, +0.01)
```