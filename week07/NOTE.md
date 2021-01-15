学习笔记
====
* 获取课程源码操作方法：
* git clone https://github.com/wilsonyin123/geekbangtrain.git
* cd geekbangtrain
* 切换分支：git checkout 6b

01變量賦值
====
1. python一切皆對象，傳遞的是對象本身，有時候是對象的引用，依此對數據類型做兩種劃分。
   1. 可變數據類型: 列表list、字典dict
   2. 不可變數據類型: 整型int、浮點型float、字符串型string、元組tuple。
2. p1_1var.py，a = [1,2,3]猶如在內存申請一個箱子空間，在箱子上貼上一個便籤a。b = a, 將b標籤貼上箱子。
3. 不可變對象，a = [4,5,6]，將貼在[1,2,3]的便籤a撕下來貼到[4,5,6]的箱子。
4. 有底層開發經驗的，可以視作malloc()申請內存。
5. 區分的目的?  
   1. 考慮性能問題，不可變優點，不管有多少可引用，都是指向同一塊內存。但每新增一個，都會消耗內存。
   2. 可變類型，值變化不會新建對象，只有內容變化或擴充。

02容器序列的深淺拷貝
====
1. 使用list(old_list)新增時，等於在內存新建一個拷貝。
2. 使用new_list = old_list[:]切片操作，也是在內存新建一個拷貝。
3. 拷貝包含子列表的列表，淺拷貝、深拷貝，只對容器序列有效，非容器、非序列則無效: 
```python
import copy 
new_list4 = copy.copy(old_list)  
new_list5 = copy.deepcopy(old_list)   #完整拷貝裡面的值，在內存新建對象

assert new_list4 == new_list5 #True 兩者相等
assert new_list4 is new_list5 #False AssertionError

old_list[10][0] = 13
```
03字典與擴展內置數據類型
====
1. 字典與哈希: 字典的key要是能被哈希，即不可變的數據類型才可做為key。
2. collections 官方文档：https://docs.python.org/zh-cn/3.7/library/collections.html
3. namedtuple 帶命名的元組p3_collections.py
```python
import collections
Point = collections.namedtuple('point', ['x','y'])
p = Point(11,y=12)
```
4. 其他包含Counter, deque
5. 用namedtuple計算兩點距離，使用numpy。p4_abc.py
```python
import numpy as np
'''
计算欧式距离
'''
vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 6])

op1 = np.sqrt(np.sum(np.square(vector1-vector2)))   
#兩個array的值相減後，分別平方，再將三個值相加後，開根號
op2 = np.linalg.norm(vector1-vector2)  
#求范數，ord = 2(默認)，為所有值平方後開根號；ord=1，array所有值絕對值的總和；ord = np.inf，求所有值的絕對值後，最大者。
```
6. 運算符重載修改__sub__的方法。
```python
class Vector(Point):
    def __init__(self, p1, p2, p3):
        super(Vector).__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def __sub__(self, other):
        tmp = (self.p1 - other.p1)**2+(self.p2 - other.p2)**2+(self.p3 - other.p3)**2
        return sqrt(tmp)

p1 = Vector(1, 2, 3)
p2 = Vector(4, 5, 6)

p1-p2
```

04函數的調用
====
1. 調用、作用域、傳入參數、返回值
2. 不帶括號，傳遞函數對象；帶括號，調用函數，傳遞值
3. 在class定義__call__魔術方法，讓實例變成可調用狀態。
```python
class Kls1(object):
    def __call__(self):
        return 123 
b = Kls1()
b() #返回123
```

05變量作用域
==== 
1. 沒有指定類型，缺點是調用參數時，可能放錯數據類型
2. LEGB規則，p1_whatis_legb.gy
   * local
   * enclosing  閉包，最有用的功能，製作成裝飾器。func內的print(y)若找不到y，會離開func去找y的值。
   * global
   * builtin
3. 作用域、查找順序

06函數工具與高階函數
====
1. 打開p1_args.py，
```python
def func(*args, **kargs):
    print(f'args: {args}')   #以tuple，將dict以外的值放到這
    print(f'kargs:{kargs}')  #將帶有key的"關鍵字參數"帶入此

func(123, 'xz', name='xvalue')

#輸出結果
#> args: (123, 'xz')
#> kargs:{'name': 'xvalue'}
```

2. 偏函數，把某一個值固定。例如: 把前四個參數固定下來，讓使用者簡單做url操作http。
```python
import functools
def add(x,y):
    return x + y
add_1 = functools.partial(add, 1)
add_1(1)

```
3. Lambda表達式，非所有函數邏輯都能封裝進去。如其他程式的匿名函數
```python
k = lambda x:x+1
print(k(1))
#如下
def       K(x): return x+1
```
4. 打開p4_hightorderfunc.py 
```python
#map叫映射，可執行的對象，後面的值會依序放到函數中去處理，再回傳給次的結果。
def square(x): 
    return x**2
m = map(square, range(10))  #返回一個對象
next(m)  #依序取值
list(m)  #一次取
list(m)  #返回空值，此迭代器已沒有值可返回

#推倒式
[square(x) for x in range(10)]
dir(m)  #查看內置屬性
```
5. reduce每兩個參數依照前面的函數做操作
```python
from functools import reduce
def add(x,y):
    return x + y   
reduce(add, [1,3,5,7,9])
```
6. filter過濾功能
7. itertools.count()計數器
```python
import itertools
g = itertools.count()
next(g)
auto_add_1 = functools.partial(next, g)
auto_add_1()
```

07閉包
====
1. 返回的關鍵字return、yield 。
2. 返回的對象--閉包(裝飾器基本的組成部位)
3. 打開p3_1closure.py~p3_6closure.py，用函數裡面再定義函數，將2與1固定。
   1. 閉包特性: 函數引用到外面的變量
```python
def line_conf():
    def line(x):
        return 2*x + 1
    return line
my_line = line_conf()
print(my_line(5))

#為何不只寫?
def line(x): return 2*x+1
print(line(5))
```
4. p3_4closure.py 固定x,y製作新的line1
```python
def line_conf(a,b):
    def line(x):
        return a*x+b
    return line
#外部函數作為初次設定
line1 = line_conf(10,1)
```
5. 引用時不用再考慮他的模式，定義ax+b, ab可以先做設定。
6. p3_5closure.py，global變數定義不會對函數裡面有影響
7. 函數和他函數外部相關聯的自由變量組合在一起稱為閉包。
```python
# nonlocal访问外部函数的局部变量
# 注意start的位置，return的作用域和函数内的作用域不同
def counter2(start=0):
    def incr():
        nonlocal start
        start+=1
        return start
    return incr
c1=counter2(5)
print(c1())
print(c1())
```

08裝飾器介紹
====
1. 在java當中當作增強語言的功能，在python則是基礎的語法
2. 猶如遊戲角色增加裝備，將無數個角色跟裝備分別做成對象並不實際，直接以裝飾器附加在角色身上，增加屬性即可。
   1. 增強而不改變原有的函數
   2. 裝器強調函數的定義態而不是運行態
3. 打開p1_decorate.py，PEP318開始引入裝飾器
4. 當裝飾器被附加到其他函數時，便會被執行
```python
def decorate(func):
    print("裝飾器被執行")
    def inner():
        return func()
    return inner
@decorate  
def func2():
    pass
```
5. 

