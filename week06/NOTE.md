学习笔记
01類屬性與對象屬性
====
1. 類，python一切接對象。某個對象有自己的特殊功能。
2. python2.2前古典類，之後有新式類，可以做class的繼承。
3. 類的兩大成員，屬性與方法。
    1. 類屬性：只存一份相同的屬性
    2. 對象屬性：不同領域不同屬性
4. 類底下的靜態字段與__init__()裡面的屬性。
5. 打開p2_class_property.py
```python
class Human(object):  #human後的()可以省略，在新式類可以繼承類。
    live = True #靜態字段
    def __init__(self, name): #self是約定俗成的命名方式，要寫其他名稱也可以，但建議用self
        #普通字段
        self.name = name 

man = Human('Adam')
woman = Human('Eve')
Human.__dict__ #查詢底下有哪些屬性
man.__dict__ #實例後有哪些屬性與變量
```
6. 用__dict__查看實例化的屬性，看不到靜態屬性
```python
man.live = False #在普通字段底下創建self.live這個屬性
man.live #輸出為False是普通字段中的live屬性
woman.live #輸出為True是靜態字段的live
```
6. 實例化的a,b是相等的嗎？值相等，但是是不同的對象，可以用__class__()查看類。同類，但內存的地址是不相同的。
7. 類也是對象
```python
c = MyClass
d = c()
d.__class__() #輸出為MyClass
```

02類的屬性作用域
====
1. 查詢類的屬性
```python
dir(Human)
Human.__dict__
Human.newattr = 1 #新增屬性
```
2. Django的寫法
```python
setattr(list, 'newattr', 'value') #不能給內置函數list添加屬性
```
3. 實例後佔不同內從，對man, woman的屬性做變更，不會互相影響。
4. 開啟p3_class_pro2.py
```python
_age = 0 #人為不可修改，中間值屬性，不建議直接修改
__fly = False #私有屬性，自動改名，不讓人修改
__init__ #魔術方法，隨環境變化
print(().__class__.__bases__[0].__subclasses__())

()
type(()) #返回是tuple的類
().__class__ #返回是tuple的類
().__class__.__bases__ #返回其父類是個object物件，但是是個元組()
().__class__.__bases__[0] #取值，從元組釋放出來
().__class__.__bases__[0].__subclasses__() #object底下所有子類和樹形結構
```
03類方法描述器
====
1. 語法糖 @，在原有的語法加上特殊的功能。
2. 普通方法self，該方法的對象。類方法cls，該方法的類。靜態方法，和類相關的功能，又不想孤立他，不能引用裡面的方法。
3. 打開p5_classmethod.py
```python
class Klsl(object):
    bar = 1
    def foo(self):
        print('in foo')
    @classmethod
    def class_foo(cls): #cls跟self一樣，是約定俗成的命名方法
        print(cls.bar)
        print(cls.__name__)  #打印Klsl隨環境變化的.__name__
        cls().foo()
Klsl.class_foo()

import django #點擊跟蹤到django的代碼，再查找@classmethod，可以查看django如何使用相印的功能
```
4. 在story裡面定義method
```python
class Story(object):
    __new__() #構造函數
    def __init__(self, name): #初始化函數，實例化時，內容都會被執行
        self.name = name
    @classmethod
    def get_apple_to_eve(cls):
        return cls.snake  

s = Story('anyone')
print(s.get_apple_to_eve())  #可以調用
print(Story.get_apple_to_eve()) #也可以調用
```
5. 何時要用classmethod？可以
    1. 特點一：參數第一個名字是類的名字cls，如同類Story()實例化成s1, s2時，調用裡面的參數就不用再用Story.name調用，可以用s1.name，可見參數self是如__name__一樣，隨環境變化，是動態語言的好處。藉此特點在父類當中建立classmethod，再用兩個子類繼承父類，調用時，值是不互相影響，各自獨立。
    2. 當函數調用的時候，需要操作類的時候。或類需要進行一系列的構造函數的時候。如同java的構造函數，但在python裡面預設只有__new__()。
    3. 打開p5_1classmethod.py
    ```python
    class Kls2():
        def __init__(self, fname, lname):
            self.fname = fname
            self.lname = lname

        @classmethod
        def pre_name(obj, name):
            fname, lname = name.split('-')
            return obj(fname, lname)

        def print_name(self):
            print(f'first name is {self.fname}')
            print(f'last name is {self.lname}')
    me = kls2('wilson', 'yin')
    me.print_name()

    #輸入改為wilson-yin, 會返回錯誤
    me2 = Kls2.pre_name('wilson-yin')
    
    ```

04靜態方法描述器
====
1. 定義好的函數，不能用到self, cls，將類裡面的屬性作轉換。
```python
class Story(object):
    snake = 'Python'

    @staticmethod
    def from
```
2. 搜尋django裡面@classmethod、staticmethod，隨便找一個功能查看。
3. 不能引用類與實例化的屬性

05描述器高級應用__getattribute__
====
1. 如果屬性不存在，則做預處理，例如給予初始值，不讓他產生異常。在類中，需要最實力獲取屬性這一行為操作，可使用：
    * __getattribute__() 對所有屬性的訪問都會調用該方法
    * __getattr__() 適用未定義的屬性
2. 開啟p6_1getattribute.py
```python
class Human(object):
    def __init__(self, name):

```
3. 開啟p6_2getattribute.py
```python
def __getattribute__(self, item):
    print(f'__getattribute__ called item:{item}')
    return super().__getattribute__(item)
    #若將super()改為self,會發生什麼結果？
```
4. 開啟p6_3getattribute.py，如果訪問屬性不存在，則給予賦值。
```python
self.__dict__[item] = 100  #__dict__魔術方法，列出類底下所有attribute
return 100
```

06描述器高級應用__getattr__
====
1. 類不存在的屬性被調用時，會被使用
2. 打開p6_4getattr.py, p6_5getattr.py
3. 當getattr與getattribute同時存在時，優先順序，p6_6both_define.py
```python
__getattribue__ > __getattr__ > __dict__
```
4. 不管屬性存在不存在，python都會調用__getattribute__，會對實例產生一定的損耗
5. 使用__getattr__時，__dict__裡依然沒有該屬性，當使用hasattr判斷是否有該屬性即使返回true，在__dict__依然看不到已經存在的屬性。雖然改變行為，但內置方法可能出現不一致的問題。

07描述器原理&屬性描述符
====
1. __getattr__與__getattribute攔截變量賦值，是底層描述器高級的實現。設置與刪除變量時也進行攔截
2. 描述器是實現特定協議的一組工具，像HTTP協議，透過瀏覽器、request服務包實現戶端與服務端。
3. 描述器更底層是描述符property，屬性描述符
```python
class Teacher:
    def __init__(self, name):
        self.name = name
    def __get__(self): #讀取
        return self.name
    def __set__(self, vale): #設置
        self.name = value

pythonteacher = Teacher('yin')
```
4. Django中的property，site-packages/django/db/models/base.py
5. 打開p7_1descraptor.py
```python
class Desc(object):

```
6. 經常用的不是底層協議，是了解後，直接用property，打開p7_2descraptor.py。將方法封裝成屬性。
```python
＠property
def gender(self):
    return 'M'
#與一般方法不同，只是單純地給予賦值，只有讀取的功能，無法在物件實例化後，進行值的修改。

class Human2(object):
    def __init__(self):
        self._gender = None
    @property
    def gender2(self):
        print(self._gender)
    
    @gender2.setter #對gender2屬性進行修飾
    def gender2(self, value):
        self._gender = value
    
    @gender2.deleter
    def gender2(self):
        del self._gender

h = Human2()
h.gender2 = 'F' #會執行self._gender = 'F'
del gender2  #執行del self._gender
```
7. 另一個property的寫法
```python
gender = property(get_, set_, del_, 'other property')
#分別用三個方法修飾gender
```
8. 建議：被修飾的函式建議用相同的函式名稱
9. 並非沒有定義setter property就不能對其寫入，gender被改名為_Article__gender。知道這些並非要自己去修改，而是要避免被其他安全工程師利用。哪些應用用到改名機制？
10. property其實是一個類，不是函數，而是特殊類，實現數據描述符的類。
    * 同時定義__get__(), __set__()方法，為數據描述符
    * 僅定義__get__()方法，稱為非數據描述符
11. 優點：方便管理屬性，控制訪問權限
```python
#property 純python實現
class Property(object):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
            self.__doc__ = doc
```
12. 打開p8_1demo.py
13. 打開p8_2demo.py

08面向對象編程-繼承
====
1. missing解決多繼承的關係
2. 重載
3. 多態，python更重視鴨子類型
4. 經典類：內建與自訂的類，父類不同，自訂的字典與原有的數據類型不一致。2.2之後，使用新式類，所有類都繼承自一個名為object的父類，無論class Human(object)有沒有加這個括號，都是新式類。
5. type這個類，很多都是繼承自type嗎？
    * object和type都屬於type類（class 'type'）
    * type類由type元類自身創建的，object類是由元類type創建。誰創建類，不一定是他的父類。
    * object的父類為空，沒有繼承任何類
    * type的父類為object類（class 'object')
6. 類的繼承
    * 單一繼承
    * 多重繼承
    * 菱形繼承
    * 繼承機制MRO
7. 打開p1_inheritance.py
8. 打開p2_inheritance.py，打name定義到父類People裡面
```python
super().__init__(name)
#先前getattribute的例子中
return super()._＿getattribute__() #引用原有的getattribute
```
9. 對象是由誰來創建的？ object.__class__，是由type創建。繼承自誰？object.__bases__，返回空，因為object不繼承自任何類。
10. type類也是type, type的父類為object。
11. 繼承多個父類，若有多個相同功能，打開p3_diamond.py，菱形、鑽石形的繼承關係。
    * 經典類：深度優先
    * 新式類：廣度優先
    * python2, 3使用不同的算法，所以新式類還是在類後面加上(object)，以免意外結果。
    * 分析繼承關係的函數，.mro顯示當前的類有沒有父類，自動繼承階層分析。
    * 手動梳理繼承關係，C3算法，有向無環圖DAG(Directed Acyclic Graph)。
    * 找到入度為零的節點為1開始找，從左邊開始找起，再從2開始找。

09solid設計原則與設計模式&單例模式
====
1. 設計原則
    * 單一責任原則the single responsobility principle：每個類負責單一的功能
    * 開放封閉原則the open closed principle：將基本功能寫在父類，子類繼承後，再進行建構、修改。
    * 里氏替換原則the liskov substitution principle：子類實現的方法，完整覆蓋父類，否則無法識別對應的對象和屬性。
    * 依賴倒置原則the dependency inversion principle：高層模塊不應該依賴低層模塊，若有依賴關係，需要對u兩者關係作抽象。
    * 接口分離原則the interface segregation principle：一個接口提供的方法剛好為我們所需要，沒必要則不需要開。
2. 單例模式：
    1. 對象只存在一個實例
    2. __init__和__new__的區別：
        * __new__是實例創建之前被調用，返回該實例對象，是靜態方法
        * __init__是實例對象創建完成後被調用，是實例方法
        * __new__先被調用，__init__後被調用
        * __new__的返回值（實例）將傳遞給__init__方法的第一個參數，__init__給這個實例設置相關參數
3. 實現方式p1_single.py，使用裝飾器使用。推薦用第二種__new__的方式，針對單線程的，如果用在多線程，要加鎖，以免被覆寫。
```python
class Singleton2(object): 
    __isinstance = False #默認沒有被實例化
    def __new__()

```
4. 引入threading，if cls in cls.objs，如果cls在對象裡面，已經實例化，則進行返回。
    1. 創建實例的部分會有問題，須先用threading.lock().acquire()加鎖。值翔完成後，finally釋放掉。
    2. 雙檢測，加鎖前後都檢測，確保多線程的運作。
5. 最簡單方法，使用模塊import的方式，import的機制是線程安全，已經引入的模塊，不會重複引入。

10工廠模式
====
1. 打開p2_factory.py，根據傳入的參數不同，建立不同的實例。靜態工廠模式
2. 類工廠模式，生產類的，factory2。通過函數的返回值，Scrapy跟Django有很多相應的功能。