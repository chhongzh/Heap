# 关于cppheap

很高兴, 第一个`cppheap`版本已正式发布.

先来说说功能吧, `cppheap`其实是我在**2023.9.21**就打算开发的了, 最开始的想法是通过`python`->`c`->`binary`的思路来实现. 这样可以用最少的代码实现最大的功能.

但是问题就在这, Python太难编译了. `nuitka`, `cython`, `pyinstaller`等, 编译后的结果十分不理想. 运行速度巨慢. 这导致开发进度缓慢.

直到**10.2**日, 我突发奇想, 打算删除python这一过程, 进化为`cpp`->`binary`.

历时不到**9**天的忙碌, 今天, 发布了

**第一个cppheap版本**

原理其实很简单, 但是却通过最简单的方法实现.

请看下面一组数据:

| data           | heap(raw code)    | cppheap        | go(raw code)   | go(With args `-ldflags="-s -w"`) |
| -------------- | ----------------- | -------------- | -------------- | -------------------------------- |
| File-Size      | 27 **byte**       | 85 **kb**      | 71 **byte**    | 1.4 **mb**                       |
| Run-time       | 0.061s            | 0.005s         | 0.158s         | 0.263s                           |
| Cross platform | need "python" env | need recompile | need "go" env. | one compile with all platform    |

总体来说, 还是时可观的.

