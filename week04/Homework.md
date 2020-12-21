01爬蟲，先將建立database並將資料寫入
====
1. 獲取資料，實例化res_get
```python
import requests

html = 'https://movie.douban.com/subject/27113517/comments?sort=new_score&status=P'

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "movie.douban.com",
    "Referer": "https://movie.douban.com/explore",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}
# 獲取索引頁
try:
    response = requests.get(url=html, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        res_get = response.text
except RequestException:
    print('獲取索引頁錯誤')
    time.sleep(3)
```
2. 引用beautifulSoup解析
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(res_get, 'html.parser')
tables = soup.select(".comment-item")

comments = []
star = {'很差':1, '较差':2, '还行': 3, '推荐':4, '力荐':5}
for i in range(len(tables)):
    tmp = (i+1,
           tables[i].select(".short")[0].text,
           star[tables[i].select(".rating")[0]['title']],
           tables[i].select(".comment-time")[0].text.strip()
          )
    comments.append(tmp)
```
3. 用pymysql寫入testdb，寫入之前，先在django建立好表格
```python
import pymysql
db = pymysql.connect("server","username","password","testdb")
try:
    # %s是占位符
    with db.cursor() as cursor:
        sql = 'INSERT INTO douban_comments (id, content, star, updated_date) VALUES (%s, %s, %s, %s)'
        cursor.executemany(sql, comments)
    db.commit()

except Exception as e:
    print(f"insert error {e}")

finally:
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)
```

02創建django project: nomeworkweek04, app:douban, table: Comments
====
1. 編輯models.py，再執行python manage.py makemigration, migrate
```python
from django.db import models

# Create your models here.
class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=255)
    star = models.IntegerField()
    updated_date = models.CharField(max_length=20)
```
2. 編輯urls，將路徑導向views的index()及index.html
```python
#Project folder底下的urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('douban.urls')),
]

#App folder底下的urls.py
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index)
]
```
3. 編輯app douban底下的views.py
```python
from django.shortcuts import render
from .models import Comments

def index(request):
    #獲取查詢關鍵字
    q = request.GET.get('q')
    error_msg=''

    if not q:
        c_lst = Comments.objects.filter(star__gte='4')
        return render(request, 'index.html', locals())

    c_lst = Comments.objects.filter(content__icontains=q)
    if len(c_lst) == 0:
        error_msg='沒有與關鍵字相符的結果'
    return render(request, 'index.html', {'error_msg':error_msg, 'c_lst':c_lst})
```
4. 在douban app底下新建static與template，將css放數static，index.html放入templates
```html
<!-- 上端用static標籤，將js與css文件連接 -->
{% load static %}
<link rel="stylesheet" href="{% static "css/bootstrap.min.css"%}">
<script src={% static "js/jquery.slim.min.js"%}></script>
<script src={% static "js/bootstrap.min.js" %}></script>

<!-- 用for迴圈將query結果帶入頁面 -->
{% for c in c_lst %}
    <tr>
        <th>{{ c.id }}</th>
        <td>{{ c.content }}</td>
        <td>{{ c.star }}</td>
        <td class="text-nowrap">{{ c.updated_date }}</td>
    </tr>
{% endfor %}
```
5. 確認views的ORM sql代碼是否正確，可以透過python manage.py shell做測試是否為需要的結果。
6. 最後執行python manage.py runserver察看結果。
