# If

if是一个块语句, 用于条件判断

```
if <Value 1> <Op> <Value 2>:
    <Statement>
else:
    <Statement>
endif

# If-elif
if <Value 1> <Op> <Value 2>:
    <Statement>
elif:
    <Statement>
endif

# If-elif-else
if <Value 1> <Op> <Value 2>:
    <Statement>
elif:
    <Statement>
else:
    <Statement>
endif
```

其中`Value1`与`Value 2`必须是个[切确的值](../define/value.md), 不能是其他任何东西.

`Op`可以是`equal`,`notequal`,`small`,`big`,`bigeual`,`smallequal`的一种.

[返回上级](index.md)