# While

While是一个块语句, 用于循环

```
while <Value1> <Op> <Value2>:

endwhile
```

其中`Value1`与`Value 2`必须是个[切确的值](../define/value.md), 不能是其他任何东西.

`Op`可以是`equal`,`notequal`,`small`,`big`,`bigeual`,`smallequal`的一种.

## 示例
```
while 1 equal 1:
    push 1;
    print;
endwhile
```

[返回上级](index.md)