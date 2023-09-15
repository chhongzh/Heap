# Func 语法

用于定义一个函数.

```
func <Name> <Arg 1> <..Arg N>:
    <Statement>;
endfunc
```

其中, **Name**是函数的名称, **Arg**代表参数. 如果在同一个上下文的情况下, 出现了重复的函数名, 则视为重载.

## 示例
```
func foo:
    # bar
endfunc

func bar foo:
    # foo
endfunc
```

[返回上级](index.md)