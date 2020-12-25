学习笔记

01為什麼使用中間件&緩存的類別
====
1. 緩存
   1. 併發數量大，數據庫無法扛住併發壓力。
   2. 複雜場景解偶，消息隊列
   3. 場景豐富造成訪問熱點
2. 緩存分類
   1. 本地緩存: 存在應用程序如Django，時間效率較高
   2. 分布是緩存: 遠程，若本地沒有，則到後端，通常是Redis。容量較高
   3. 思考: 
      1. 各自存儲數據的特點是甚麼?
      2. 各自適合的場景是甚麼?  ex: 分布式 遊戲排名、排行

02緩存的同步方式有哪些
====
1. cach aside讀取緩存，如果用戶請求有，就返回，若沒有則向數據庫請求到緩存。優點容易理解，缺點對業務代碼侵入。
2. write back, 用消息對列每隔一個時間同步到數據庫。但可能數據丟失的風險。對一致性要求不高的場景。 
3. 寫入方式
   1. 雙寫方式: 多線程，容易實現，但也容易緩存、數據庫不一致。改變方式，先寫數據庫、再寫緩存。
   2. 消息隊列: 當數據庫寫入成功後，再寫入緩存。要考慮程序cash時，消息隊列的訊息不會丟失。
   3. MySQL Binlog二進制日誌: 最穩定，但是是線性的，性能最差。
4. 都會有訊息不一致性和性能延遲的問題。

<img src="./images/03.png" style="height:300px" />

03緩存可能出現的問題
====
1. 緩存穿透
   1. 人為的分布式拒絕服務攻擊
   2. 若查詢結果是空值，可以直接到redis裡面存null結果
   3. 布隆過濾器，有誤殺的概率
2. 緩存併發
   1. 值存在，但某一個key過期，但剛好大量用戶請求
   2. 互斥鎖, redis的setnx，
3. 緩存雪崩:
   1. redis設置不合理，緩存大量的key，同一時間過期，大量的請求經過redis進入數據庫。
   2. 不讓大量的key同時失效。
   3. 多級緩存，大量併發不要同時打到數據庫。

04安裝Redis、連接Redis
====
1. Redis 6.0後開啟多線程的技術，作為緩存來用，類似mysql的數據庫。
2. 舊版多個會話會相互干擾
3. 對象類型
   1. 字符串: int超過八個字節，會轉換成embstr或raw，建議使用時將key固定在8個字節以內。字節過多會佔過多空間。
   2. 列表: 時間換空間的存儲。
   3. 哈希
   4. 集合: 
   5. 有序集合
4. 安裝redis-6.0.9版本
```Shell
#需先將gcc 版本從4.8.5升級到8.0
yum install centos-release-scl scl-utils-build
yum list all --enablerepo='centos-sclo-rh'
yum install -y devtoolset-8-toolchain
#安裝完後以以下指令啟動
scl enable devtookset-8-toolchain
gcc --version
#在centOS的系統，先從根目錄進入redis-6.0.9目錄
cd redis-6.0.9
make ; make install 
#安裝完成後，redis會有以下文件
which redis-server
#返回/usr/local/bin/redis-server
which resis-cli
#返回/usr/local/bin/redis-cli   
#redis-6.0.9目錄下會有redis.conf配置文件，可以修改工作方式。可以複製到etc下面，來更改redis.cnf配置文件
vim /etc/redis.cnf     
:set nu  #在vim編輯器中顯示行號
#找到requerspass，將密碼修改得足夠複雜
#找到bind，將ip改為0.0.0.0 監聽所有ip位置。
:wq #寫入後退出vim編輯器

#啟動redis
redis-server /etc/redis.conf
ss -ntpl | grep 6379  #過濾端口，查看redis是否正確啟動起來。
#關閉redis
redis-cli  ##進入redis
127.0.0.1:6379> auth yourpassword
127.0.0.1:6379> shutdown
```
5. 在python如何連接redis
```shell
pip install redis
```
開啟mod5_redis_conn.py
```python
import redis
client = redis.Redis(hots='server1', password='pass')
print(client.keys()) #連接測試，生產環境不要用此指令。返回列表，bytes。
for key in client.keys(): 
   print(key.decode())
```

05Redis字符串使用場景
====
1. 打開mod5_redis_string.py
```python
#主要用set跟get來做溝通

client.set('key', 'value')
result = client.get('key')

print(result.decode())
```
2. 即使遇到相同的key，set會覆蓋掉原有的值，可用nx=True參數，讓key的value不被後續set()更改
```python
client.set('key', 'value2', nx=True) #若遇到key已經存在，不會覆寫該key的value
result = client.get('key') 
print(result.decode())
#輸出結果仍是value，而非value2
```
3. 修改字符串，為key後面增加字符
```python
client.append('key', 'value4')
result = client.get('key') 
print(result.decode())
# >> valuevalue4
```
4. 值的加減
```python
client.set('key2', '100')
result2 = client.incr('key2') #+1
result3 = client.decr('key2') #-1
print(result2)  #101
print(result3)  #100 
```
5. 字符串大部分是紀錄映射關係，將數據存到內存到中，查詢會非常快。用戶都入之後，從數據庫寫入redis，後續用戶直接從redis查詢，會非常快速。
6. 字符串只用在小量的資料，百萬級以下可以；若超過百萬，則要用哈希，消耗的內存只有字符串結構1/4的大小，查詢效率卻是相同的。
7. 查詢單個key，可以使用get()，但查詢所有的key，可以用keys*，就像sql的select *，但這時會造成redis短暫無法響應的情況，因為要把所有key列出來。若數據量達到百萬，無法響應的時間可能會達到秒級。若不清楚有多少key之前，不要輕易用key*這樣的指令。

06Redis列表
====
1. 打開mod5_redis_list.py  
```python
# index也支援負索引-1，跟python一樣
client.lpush('list_redis_demo', 'python') #從左側填入列表
client.rpush('list_redis_demo', 'java') #從右側
#不要盲目把所有資料拉出來，先看長度
print(client.llen('list_redis_demo')) #list的length
# 彈出數據 lpor()  rpop()
data = client.lpop('list_redis_demo') #輸出 b'python'
print(data)

#查看一定範圍的list數據
data = client.lrange('list_redis_demo', 0, -1) 
print(data)
```

2. 實際場景中，當作隊列用，批量做事情。短信網關有併發限制，先存入redis中，分批發送。其中沒有成功的用戶，再重新發一次。發送成功則rpop()彈出，若沒有成功則lpush()放回隊尾，確保所有用戶都發送成功。
3. 循環發送
```python
while True:
   phone = client.rpop('list_redis_demo')
   if not phone:
      print('發送完畢')
      break
   # sendsms(phone)
   # result_time = retry_once(phone)
   # if result_times >= 5:
   #    client.lpush('list_redis_demo', phone)
```
4. redis用於批量發短信、通知、禮物等，可處理大量資料。

07Redis集合(set)
====
1. 往集合添加值
```python 
print(client.sadd('redis_set_demo', 'new_data'))  #成功添加進去返回1，若以包含相同內容，則會添加失敗，返回0
client.spop() #隨機彈出，真的隨機數
client.smember('redis_set_demo') #顯示

#最有用的兩個集合的運算
#交集
client.sinter('set_a', 'set_b')     #a已經買尿布的人, b已經買啤酒的人

#並集
client.sunion() 

#差集
client.sdiff() 
```
2. 去重，丟入集合自動完成；兩個集合的交集、並集、差集。

08Redis哈希
====
1. 查詢單個key的時候，查找時間都不會增加。應用紀錄用戶是否為VIP，對應值設為1，反之刪除或設為0。
2. 增加和刪除
```python
client.hset('vip_user', '1001', 1) #新增
client.hset('vip_user', '1002', 1)     
client.hdel('vip_user', '1002') #刪除

print(client.hexists('vip_user', '1002')) #查找是否存在
```
3. 存字符串或哈希? 哈希優化更好，佔用內存小很多。例如: instagram使用python開發，從字符串轉為哈希，節省內存從十幾G降到5G。
4. 批量添加大量值
```python
client.hmset('vip_user', {'1003':1. '1004':1})
#讀取值，hkeys  hget  hmget  hgetall，其中hmget逐漸被取代，主要掌握其他三個。
field = client.hkeys('vip_user') 
print(field)  #返回結果  [b'1001', b'1003', b'1004']
print(client.hget('vip_user', '1001'))  #取得一個字段  b'1'
print(client.hgetall('vip_user'))  #取得所有用戶與值  {b'1001':b'1', b'1003': b'1'}
```
5. 遇到取得出來，取不出來的。不能用return的方式判斷，而是print的結果來判斷。
6. 取出來是bytes，需要用for迴圈迭代的方式，decode()轉換
7. Redis哈希比起字典，除了key, value，還多出name，用name對應業務各種關係，儲存大量數據且效率極高。

09Redis有序集合
====
1. 