作业一：
====
区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
1. 容器序列：存放的是它们所包含的任意类型的对象的<b>引用</b>。猶如向內存申請一個盒子，並在盒子上貼上標籤，即使修改裡面的元素，佔用的記憶體位置仍不改變。
    * list, tuple, dict, collections.deque
2. 扁平序列：存放的是<b>值</b>而不是<b>引用</b>。
    * str
3. 可變序列：值變了，記憶體位置不一定改變。
    * list
    * dict
    * collections.deque
4. 不可變序列：值變了，記憶體位置一定變。
    * str
    * tuple

作业二：
====
* 自定义一个 python 函数，实现 map() 函数的功能。
```python
def func(a):
    return a**2

lst = [1, 2, 3, 4, 5]
print(list(map(func, lst)))
```

作业三：
====
* 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。

```python
from datetime import datetime
import time
def timer(func):
    def decorater(*args, **kwargs):
        cur = datetime.now()
        ret = func(*args, **kwargs)
        print(f'運行時間：{datetime.now() - cur}. ')
        return ret
    return decorater

@timer
def foo1(a: int, b: int):
    time.sleep(5)
    return (a + b)

foo1(1, 2)
```