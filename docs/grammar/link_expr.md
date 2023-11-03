# 链式调用

一种调用函数的方式.

```
<obj> -> <Func Name> <arg>... ;
```


## 示例
```
# Call foo with link expr:
"Foo!" -> foo;
# foo 会接收到 "Foo!"

"Foo!" -> foo -> bar;
# bar 会接收到 foo 处理的结果

```

[返回上级](index.md)