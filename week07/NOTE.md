学习笔记
====
* 获取课程源码操作方法：
* git clone https://github.com/wilsonyin123/geekbangtrain.git
* cd geekbangtrain
* 切换分支：git checkout 6b、git checkout 7a

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
5. 用包裝的方式簡化code
```python
# 注册
@route('index',methods=['GET','POST'])
def static_html():
    return  render_template('index.html')

# 等效于
static_html = route('index',methods=['GET','POST'])(static_html)()


def html(func):
    def decorator():
        return f'<html>{func()}</html>'
    return decorator

def body(func):
    def decorator():
        return f'<body>{func()}</body>'
    return decorator

@html
@body
def content():
    return 'hello world'

content()
```

09被裝飾函數帶參數和返回值的處理
====
1. 被裝飾的函數帶參數，該如何寫？打開p3_function_args.py
```python
# 被修饰函数带参数
def outer(func): 
    def inner(a,b):
        print(f'inner: {func.__name__}')
        print(a,b)
        func(a,b)
    return inner

@outer
def foo(a,b):
    print(a+b)
    print(f'foo: {foo.__name__}')
    
foo(1,2)
foo.__name__
```
2. 被包裝後，當呼叫foo()時，事實上是呼叫inner()，意義上foo(1,2)等同於inner(1,2)。func名稱仍是在全域環境下的foo。inner內的func被呼叫時，打印出foo.__name__為foo，因包裝時，return inner 給foo，所以foo.__name__會是inner。
    1. 函數已經被替換成裝飾器的內部函數
    2. 當函數帶有兩個參數，inner內部函數也需要同時帶兩個參數，才能把原有的參數帶給foo。
3. 把內部函數改為接受，不定參數的格式
```python
def outer2(func):
    def inner2(*args, **kwargs):
        #在此加入新的功能
        ret = func(*args, **kwargs)
        return ret  #讓foo2
    return inner2

@outer2
def foo2(a,b,c):
    return a+b+c

foo2(1,3,5)
```
4. 需要關注的
    1. 到底用的是函數的對象名稱，還是讓你的函數運行起來拿到結果。
    2. 函數裡邊的作用域
    3. 參數
    4. 返回值：在內部函數修改返回值
```python
#打開p4_decorate_args.py
# 装饰器堆叠

@classmethod
@synchronized(lock)
def foo(cls):
    pass


def foo(cls):
    pass
foo2 = synchronized(lock)(foo)
foo3 = classmethod(foo2)
foo = foo3
```

10Python內置裝飾器
====
1. 最常用functools，cache緩存
2. 打開p5_wraps.py，建議使用functools.wraps的方法做裝飾，以及LRUCache，多次調用函數，且結果一致時，直接返回結果即可，不用再執行函數。
3. LRU是一種淘汰機制，打開p6_lru_cache.py
```python
import functools
@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
```

11類裝飾器
====
1. 打開p7_class_decorate.py，用class作為裝飾器。
2. 打開p8_decorate_class.py，使用@decorate重寫dislay
3. 用__call__將class模擬成函數(可調用的對象)，

12官方文黨中的裝飾器代碼閱讀指南
====
1. 打開p9_other.py，新版本更新，可以觀察文檔學習發展趨勢。
2. PEP會描述那些功能會即將過期，或為何要新增那些功能。
3. Data class的功能，python 3.7版本新增，省掉__init__與__eq__的編寫，但var_a不能作為類屬性訪問。
```python
from dataclasses import dataclass   
@dataclass
class MyClass:
    var_a: str  
    var_b: str
```

13對象協議與鴨子類型
====   
1. Duck Tpying定義: 按照字典的方式訪問你，可以得到相應的結果，就把你當作字典。
   1. 透過容器類型協議: 
      1. __str__
      2. __getitem__, __setitem__, __delitem__ 字典索引操作
      3. __iter__迭代器
      4. __call__可調用對象協議
   2. 比較大小的協議:
      1. __eq__
      2. __gt__
   3. 描述符協議和屬性交互協議
      1. __get__
      2. __set__
   4. 可哈希對象
      1. __hash__
2. 自己編寫的程序要跟標準的函數對齊。例如: 定義班級class，用__iter__顯示班級人數，便能用len()函數來對班級類操作。
3. 可哈希，即字典，自己定義的類要使用字典模式，就要用__hash__
4. 上下文管理器，with使用__enter__()、__exit__()操作完文件finally自動關閉文件。
5. 打開p2_FormatSring.py，一般情況__str__跟__repr__會設定相同的值。
6. 格式化字符串
7. 用print正常輸出會用__str__，程序調用會用__repr__。
8. 類型註記typing，與鴨子類型相反，聲明變亮的時候就要指定類型，如果使用其他類型對變量賦值就會報錯。
   1. 大型的程序需要傳遞參數，提示應該怎麼輸入，只是提示，不能強制。強制定義對動態語言沒有意義。
```python
def func(text:str, number: int) -> str:
    return text*number
func('a',5)
```

14yield語句 p1_iter.py
====
1. return 的返回比較直觀，有多少值，全部一起返回。
2. yield: 返回生成器。用for in取值，則有暫停功能，每次取一個值。
```python
a = (i for i in range(1,10))
next(a)
for i in a:
    print(i)
```
3. 能以next與for in取值的功能，即為完成的迭代器。
4. iterables，有__iter__一定是可迭代，可用for in；有__iter__且有next()，則為iterator；若進一步包含yield，則為generator。
5. 打開p1_iter.py
```python
alist = [1,2,3,4,5]  
hasattr(alist, '__iter__') #True
hasattr(alist, '__next__') #False   
#實務上常以此判斷是否有相應屬性，若無則用setattr()添加，動態變化。

for in in alist:
    print(i)
#list可迭代，但不是迭代器
```
6. 用class實現__iter__和__next__就能實現迭代器，
7. 用函數def實現迭代器協議，最簡單。只要用yield，不用寫iter與next，def返回的訊息就是"生成器對象"，執行之後變成"生成器構造函數"。
8. 若不確定是否為生成器，可以用check_iterator()進行檢測

15迭代器使用的注意事項
====
1. C++裡面也有，python的迭代器沒有C++那樣完整。
2. yield並不會比較省內存，而是實現迭代器的協議，只用next就可以調用他。
3. 打開p2_infinite.py，計數、循環、重複
4. 有限迭代器，避免多次循環
```python
for j in itertools.chain('abc', [1,2,3]): 
    print(j)
```
5. python3.3  引入yield from
```python
def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i
def chain(*iterables):
    for i in iterables:
        yield from iterables #替代內循環
s = 'ABC'
t = [1, 2, 3]
list(chain(s, t))
```

6. 打開p3_destroy.py，定義好迭代器後，從後面插入值。字典若再被插入新值，迭代器會失效。
7. 列表若插入新值，迭代器只會變長，不會失效。
8. 迭代器一旦耗盡，永久損壞。裡面內容只能取一次，與列表不同。