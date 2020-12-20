学习笔记
获取课程源码操作方法：
git clone https://github.com/wilsonyin123/geekbangtrain.git
cd geekbangtrain
切换分支：git checkout 5a

01
====
pip install --upgrade django==2.2.13  # 指定版本安裝
若已安裝，到python後import來查詢
>>>import django
>>>django.__version__
MTV架構，model, template, view

02創建項目和目錄結構
====
1. django-admin startproject Mydjango #自訂名稱，產生目錄結構。python manage.py 命令工具，python setting.py 項目的配置文件，以上只是框架
2. 創建應用程序，python manage.py startapp index #命名為index的應用程序。底下有models.py模型與views.py視圖，template.py則要手動去創建
```Shell
django-admin startproject MyDjango
python manage.py help #列出manage可執行的命令

python manage.py startapp index
find index/ #列出index底下的內容架構
python manage,py runserver #讀取默認的MyDjango.settings配置文件，並顯示環境位置為http://127.0.0.1:8000/，在瀏覽器可以透過該網址查看內容。
```
3. 啟動和停止Django應用程序，按ctrl + c可以終止運行
```Python
python manage.py runserver #默認是127.0.0.1:8000
python manage.py runserver 0.0.0.0:80  #如果希望其他人也可訪問，可改成此。實際應用時，端口號可能比8000更大，且是隨機的
```
03解析settings.py主要配置文件
====
1. 入口為manage.py，他的配置存在settings.py，包括
* 項目路徑
BASE_DIR = os.path.dirname() #讀取路徑的基本套路
* 密鑰：建議大家去修改，防止跨站入侵
* DEBUG：調適模式，僅適用開發環境
* INSTALLED_APP: django默認程序，不要修改他的次序，他是從上到下陸續加載。若不要用到，則註釋掉不要刪；新增自己的，則往後加入。若沒有將自己的app放入，程序自然不會被加載。
* MIDDLEWARE中間件：從上到下執行依順序加載，若不熟悉中間件，不要更動。
* ROOT_URLCONF: 當進行http請求，django針對哪個url進行匹配，統一字源定位符的配置。
* Template模板設置：
    * BAKEND: 定義模板引擎，若要改用Flask框架的jingia模板，可在此設置。
    * DIRS: 設置模板路徑，一般不在這設置，而是在app裡邊設置模板。所以app_dirs設為true。
    * 後續的基本上不去改動。
* WSGI配置
* DATABASE指定數據庫，預設為SQLite，但通常改為其他數據庫。
    * 將SQLite的配置註釋掉。
    * 修改為
    ```Python
    DATABASES = {
        'default': {  #默認第一個數據庫可以命名為default, 若多個數據庫，其他要用有意義的命名。
            'ENGINE': 'django.db.backend.mysql',
            'NAME': 'test', 
            'USER': 'root',
            'PASSWORD': 'rootroot', 
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    DATABASES = {
        'db1': {  #默認第一個數據庫可以命名為default, 若多個數據庫，其他要用有意義的命名。
            'ENGINE': 'django.db.backend.mysql',
            'NAME': 'mydatabase', 
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword', 
            'HOST': '127.0.0.1',
            'PORT': '3307',
        }
    }
    ```
    * 以上配置後，還不能正常使用，由於把驅動引擎SQLite已經換掉，Django連接MySQL還差一個引擎。使用mysqldb或pymysql的包去實現。若直接執行會報錯誤OSError: mysql_config not found，因為找不到mysql客戶端的命令，需要執行以下動作
    ```Shell
    pip install pymysql    #安裝pymysql以找到mysql的配置，解決客戶端的問題
    export PATH=$PATH:/usr/local/mysql/bin #安裝完成後，若mysql客戶端安裝位置為/usr/local/mysql/bin，透過此指令導出環境配置變量，指向mysql。

    pip install mysqlclient #引擎的問題可以用pymsql解決，也可以用mysqlclient，兩者是較常用的。
    ```
    * 若pymysql版本過低，只要改掉連接相關的源代碼即可，為版本判斷的代碼作注釋。
* 密碼驗證的功能不用改
* 時區設定可以修改與實際環境相同
* 靜態文件STATIC_URL
2. 一般需要修改的只有數據庫，從SQLite改成關係型或非關係型數據庫，第二個要改是installed_apps。

04urls調度器Urlconf
====
1. 每個功能建議分成不同app來寫，例如：wiki網站底下分為登入、編輯、評論，分別建立app。	
2. 增加項目urls
```Python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')), #路徑是空，用inlude找到index這個app底下的urls.py文件。繼續在index的urls.py的內文做views視圖的解析。
]
```
2. 來到index/urls.py
```python
from django.urls import path
from . import views  # 其中 . 為相對路徑，表示index目錄名稱，與當前文件同一級別。

urlpatterns = [
    path('', views.index) #依然是空路徑，指向views底下的index函數。其中views是哪來的？即是當前目錄中的views。

]
```
3. 來到index/views.py	
```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello Django!")

```
4. 運行過程：
    1. 首先從manage.py, 底下的ROOT_URLCONF = 'MyDjango.urls', 來到app MyDjango目錄底下的urls.py
    2. 來到MyDjango的urls.py，由於網頁url是空的，在urlspatterns第一項path('admin')不匹配，所以繼續下一個，找到path('',include('index.urls'))。include綁定一個app叫做index。
    3. 程序如何找到index app? 是透過settings.py裡面的installed_apps來找到。找到index後，來到index底下的urls.py
    4. 來到index/urls.py，依然要找到urlpatterns，匹配到空路徑path('', views.index)
    5. 找到views.py內的index 函數。

05模塊和包
====
1. 模塊是.py結尾的檔案，python的優雅寫法，將定義函數與執行分開
```python
def func1():
    print('import func1')
if __name__ = '__main__':
    func1()
```
2. 包是包含許多模塊的目錄，底下會有__init__.py的檔案，會在import該包的時候，優先運行。
```Python
# 目錄MyPackage底下__init__.py內容為
print('hello')

#當其他程序import MyPackage時，會執行__init__.py的內容
>>> import MyPackage
Hello
```
3. import 多層目錄的方法
```python
from . import Module2
from .Pkg2 import Module3 as M3
```

06讓URL支持變量
====
1. 判斷數據類型以及正則表達式，Django還可以匹配自定義
2. 帶變量的URL, 支持str字符串, int數字, slug備註, uuid唯一的id, path路徑。可以直接在用戶輸入時，判斷輸入類型是否正確。
```python
path('<int:year>', views.myyear), 
#傳入的參數會賦值給year變數，賦值後若發現不是int類型，則會報錯誤
```
3. 打開index/urls.py
```python
path('<int:year>', views.year), 
#其中year的變數會傳到views.py內的year函數做匹配; 若year非整數，則Django默認返回404的錯誤。
```
4. 變量year傳到views.py內的year函數，打開index/views.py
```Python
def index(request):
    return HttpResponse("Hello world")

def year(request, year):  #帶入兩個參數，第一個是request，第二個是year變量
    return HttpResponse(year)
# python manage.py runserser後，打開連結https://127.0.0.1:8000/ ，會看到Hello workd。若是https://127.0.0.1:8000/12345，則會顯示12345。若不是輸入int，則會返回錯誤。
```
5. url上的參數是如何傳遞？
```python
#index/urls.py中
path('<int:year>/<str:name>', views.name)
#參數帶到views.py內的def name
def name(request, **kwargs):  #用**kwargs將傳送過來的參數全部帶入，作為一個dict()
    return HttpResponse(kwargs['name'])  #kwargs['year'], kwargs['name']
```
07url正則和自定義過濾器
1. (?P<year>[0-9]{4}).html, 其中?P告訴re_path後面是對應的變量，以及能匹配的正則表達式。表示year為四個數字組成。當匹配到四個數字，便傳入year變量，和後邊的.html組成“年份.html”，
```python
# urls.py
re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear')
#後面的name='urlyear'，是給後續template使用的

# views.py
def myyear(request, year):
    return render(request, 'yearview.html')
# 用render將代碼寫到指定文件yearview.html，渲染後再返回

# Templates文件夾增加yearview.html
<a href="{% url 'urlyear' 2020 %}">2020 booklist</a>
```
2. 再urls.py，需要手動import re_path。
3. 自定義匹配規則：
```python
# 假設要自定義變量myint
path('<myint:year', views.year),
# 需要以下方法註冊
from django.urls import path, re_path, register_converter
from . import views, converters
# 1. import register_converter這個function
register_converter(converters.IntConverter, 'myint')
# 2. converters.IntConverter為一個class，而converters為自己編寫的class，在該檔中自己編寫IntConverter與FourDigitYearConvert的class
register_converter(converters.FourDigitYearConverter, 'yyyy')
```
* 與urls.py、views.py同級的目錄下新建converters.py：
```Python
#首先定義個必須是一個class，且包含三個部分。
class IntConverter:
    regex = '[0-9]+' #匹配的正則，不用管他如何引入，resgister_converter會在繼承時自動引入
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return str(value)
    #以上兩者為相反的過程，進到python時，仍是str，需要轉成int才能做判斷
    #要回傳到網頁做展示時，仍要轉為string，所以要str(value)

#在urls.py中，將自定義的class做註冊，並自定義名稱為myint
register_converter(converters.IntConverter, 'myint')
```
4. 更進階的寫法
```python
#打開converters.py
class FourDigitYearConverter:
    regex = '[0-9]{4}'
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return '%04d' % value  #格式化輸出描述符

register_converter(converters.FourDigitYearConverter, 'yyyy')
# 自定義過濾器
path('<yyyy:year>', views.year),
```
5. 使用自定義匹配，就不用寫?P這樣複雜的正則，且可以做更多的不同匹配。

08view試圖快捷方式
1. response()一般的方式
|響應類型|說明|
|----|----|
|HttpResponse("Hello world")|200,請求成功|
|HttpResponseRedirect('/admin/') |http狀態碼302，重新定向到Admin站點的url|
|HttpResponsePermanentRedirect('/admin/')|301. 永久重定向Admin站點url|
|HttpResponseBadRequest('BadRequest')|400,訪問的頁面不存在或著請求錯誤|
|HttpResponseNotFound('NotFound')|404, 頁面不存在或著網頁的URL失效|
|HttpResponseForbidden('NotFound')|403, 沒有訪問權限|
|HttpResponseNotAllowed('NotAllowedGet')|405, 不允許使用該請求方式|
|HttpResponseServerError('SeverError') |500, 服務器內容錯誤|
2. Django快捷函數
* render()將給定的模板與給定的上下文字典組合再一起，並以渲染的文本返回一個httpresponse對象。
* redirect(), 將一個HttpResponseRedirect返回到傳遞的參數的適當URL。
* get_object_or_404()在給定的模型管理器(model manager)上調用get(), 但他會引發Http404而不是模型的DoseNotExist異常。從數據庫取數據，將模型和views做綁定。
3. render(), ctrl點擊，可以看到他的code
```python
content = loader.render_to_string(template_name, context, request, using=using)
#將模板和文件內容做綁定

#回到views.py, 是如何找到yearview.html? 由於在settings.py設定在app內尋找文件, 默認會在app底下的templates目錄尋找文件，該目錄需要手動創建。
render(requset, 'yearview.html')
```
4. 在index app目錄底下創建templates，並在裡面創建yearview.html，在該文件中編輯html

5. redirect(), 需要先處理，再轉到另一個url。重新回到urls.py再做解析
```python
# views.py中
def year(request, year):
    return redirect('/2020.html/')
# 如果url請求的是year(),就會轉到/2020.html/
```

09使用ORM創建數據表
====
1. 非直接操作數據庫，對象提取
2. 繼承自models.Model, 設計table, 相對應SQL的語言
3. 正向操作，manage.py makemigration 與migrate將ORM表轉成SQL。
4. AutoField自動增值
5. python manage.py會顯示需要做哪些指令做處理
6. Python manage.py makemigration 後，在目錄migrations會出現0001開頭的文件，作為修改SQL的文件，即為中間腳本
7. 運行時若發現找不到MySQL配置，須到整個project根目錄的__init__.py中配置，該文件在runserver時，都會先被運行。
import pymysql 
pymysql.install_as_MySQLdb() #替換資料庫
8. 若仍找不到，在terminal手動將MySQL加入搜索路徑 export PATH=$PATH:/usr/local/mysql/bin
9. 若遇到sql版本與decode報錯，也是追尋code將其註釋掉。
10. 在terminal登入MySQL, 查看創建的結果

10ORMAPI
====
1. 到django官方文檔認識字串、浮點數、日期等幾個常用的table欄位屬性
2. Django驗證ORM語句的shell, 打開ORM_API.txt
3. Python manage.py shell可打開練習用python 做數據的增刪改查

14urlconf與models配置
====
1. 是否要製作獨立的app? 
   * https://ip/xxx
   * https://ip/yyyy
   * https://ip/douban/www
   * https://ip/douband/yyyy
   * 為douban新建一個app
2. 實際操作
```python
>>> python manage.py startapp Douban
#打開setting.py，將'Douban'註冊到INSTALLED_APPS列表中
#當runserver時，會將app加載進來

#打開urls.py   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('douban/', include('Douban.urls'))  #Douban後面要加上/，但前面不可以加上/，否則路徑拼接時，會報錯。
    #include()函數會透過install_app的列表，找到urls.py的位置。
]
# 當網頁執行https://ip:port/douban/index後會找到douban底下的urls.py，路徑為'index'的做匹配
path('index', views.books_short), 
```
3. 藉由以上方法，可以在一個project下新增不同的app，不用擔心app之間的路徑重複的問題
4. urls.py如何確保找到的是當前app的views? 是在from . import views，確保import只從當前目錄下找views.py。
5. 打開douban底下的views.py。
```python 
#如何抓取數據? 表的結構與內容是已經創建好的，如何反向創建模型
python manage.py inspextdb > models.py
#mysql中指定的表轉換成model，並輸出到文件
#其中會多產生一個class Meta  元數據，其中內容並不屬於表中任一條紀錄
class Meta: 
    managed: False  #默認為true，方可用orm指令做數據庫的變更，由於是SQL轉過來的，django為避免更動到SQL的內容，所以預設為false。若是我們自己用ORM創建的數據庫則沒有設定這個選項，且預設為True
    db_table = 't1' #預設是"app名+下畫線+類的名字"做為表名，例如:Douban_T1。由於是SQL轉來的，會設定為原本的t1名稱。
```
6. mysql配置連接，打開settings.py中的DATABASES的列。

15views視圖的編寫
====
1. 導入模型，打開douban底下的views.py 
```python
from .models import T1 #即是透過SQL反向建立的模型

def books_shor(request):
    shorts = T1.objects.all()   #.objects()為模型的管理器

```
2. 要如何從SQL抓取需要的結果? 一般會先到mysql中，用SQL語句查看內容，根據結果寫成ORM管理器中對應語法。
4. 打開terminal: /usr/loca/mysql/bin/mysql -uroot -ppassword db1，通常以此進入
```mysql
show tables;
desc t1;
<!-- 先了解是甚麼結構、欄位類型 -->
select * from t1 limit 2\G

```
5. 編寫views，先打開django文檔說明，模型層的QuerySet
```python
#檢索全部對象
all_entries = Entry.objects.all() #此類型為QuerySet，像是dict()，可用python標準語句，如count()
plus = queryset.filter(**conditions).count()  #過濾器，包含給定查詢參數，判斷條件格式**conditions是要求dict()有key有value的格式
queryset = T1.objects.values('sentiment')
conditions = {'sentiment__gte':0.5}  #__gte為大於等於，常見gt大於、lt小於、gte、lte大於等於、小於等於
```
6. 聚合函數找平均星等，找到django官方文檔，需要用到avg函數。
```python
star_avg = f" {T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
#aggregate返回的是dict()，用['n_star__avg']抓取結果值；:0.1f是f-string的功能，顯示小數一位
```

16結合bootstarp模板進行開發
====
1. 打開templates目錄與static底下的css等目錄。
2. 找到starbootstrap.com 
3. 珊格系統
4. 在views.py中，locals()會將當前函數下所有屬性進行加載
5. {{block.super}}，可將父級的內容進行保留、加載進來，否則會被覆寫。







	
