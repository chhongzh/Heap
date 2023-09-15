# Iter 语法

遍历元素.

```
iter <List> <Var Name>:
    <Statements>;
enditer
```

**List**是需要遍历的对象, 而**Var Name**就是遍历的结果将会存在哪里.

## 示例
```
iter [1,2,3,4] i:
    get i;
    print;
enditer
```

[返回上级](index.md)