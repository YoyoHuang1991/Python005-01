1.在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
====

* 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交 

 ```mysql
 ALTER DATABASE testdb CHARACTER SET utf8mb4;
 ```

* 将增加远程用户的 SQL 语句作为作业内容提交

 ```mysql
CREATE USER 'testuser'@'%' IDENTIFIED BY 'testpass';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%';
 ```

2.使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
====

* 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
```Python
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime 
from sqlalchemy import DateTime

Base = declarative_base()

class Member_table(Base): 
    __tablename__ = 'member' 
    member_id = Column(Integer(), primary_key=True) 
    member_name = Column(String(15), nullable=False, unique=True)
    member_age = Column(Interger())
    member_birth = Column(DateTime())
    member_sex = Column(String(5))
    member_education = Column(String(20))
    created_on = Column(DateTime(), default=datetime.now) 
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"《用戶表》中的用戶id={self.member_id}, \n用戶名稱：{self.book_name}"

dburl="mysql+pymysql://testuser:testpass@172.16.129.2:3306/testdb?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)
# 实例一个引擎
#其中參數為：
# 1. 資料庫使用者：testuser
# 2. 資料庫使用者密碼：testpass
# 3. 資料庫ip位置與port：172.16.129.2:3306，我是使用xampp的mariaDB
# 4. 資料庫名稱：testdb

```
* 将 ORM、插入、查询语句作为作业内容提交
1. 建立session
```Python
# 创建session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()
```
2. 用session增加数据
```Python
member_demo = Member_table(member_name='新之助',
                        memeber_age=5,
                        member_birth='1991-10-10',
                        member_sex='male',
                        member_education='雙葉幼稚園',
                        )
session.add(member_demo)
session.commit()
```
2. 用session查詢
```Python
all_result = session.query(Member_table).all() #顯示所有Member_table的資料
first_result = session.query(Member_table).first() #只抓第一個結果
result = session.query(Member_table).filter(
    and_(
        Book_table.memberid.between(1, 5),
        Book_table.member_name.contains('新')
    )
).all()) 
#找到member table中，id在1到5之間，且member_name包含‘新’的結果。
```

3.为以下 sql 语句标注执行顺序：
====
```mysql
SELECT DISTINCT player_id, player_name, count(*) as num     #5 查詢player_id與player_name不重複，並計算數量
FROM player JOIN team ON player.team_id = team.team_id      #1 join player與team兩個表，產生虛擬表
WHERE height > 1.80                                         #2 篩選條件為height大於1.80者
GROUP BY player.team_id                                     #3 以player.team_id分組，各組有多少height大於1.80
HAVING num > 2                                              #4 其數量num大於2者
ORDER BY num DESC                                           #6 結果輸出的排序為降冪
LIMIT 2                                                     #7 顯示結果的前兩筆資料
```

4.以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?
====
### Table1
|id |name|
|----|----|
|1 |table1_table2|
|2 |table1|

### Table2
|id |name|
|----|----|
|1 |table1_table2|
|3 |table2|
以下代碼INNER JOIN替換為LEFT與RIGHT的不同結果
```mysql
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;
```
* INNER JOIN的結果選出兩表id相同者，僅一筆資料

|Table1 . id |Table1 . name|Table2 . id|Table2 . name|
|----|----|----|----|
|1|table1_table2|1|table1_table2|

* LEFT JOIN的結果，兩表id相同外，亦把table1的內容抓出來

|Table1 . id |Table1 . name|Table2 . id|Table2 . name|
|----|----|----|----|
|1|table1_table2|1|table1_table2|
|2|table1|none|none|

* LEFT RIGHT的結果，兩表id相同外，亦把table2的內容抓出來

|Table1 . id |Table1 . name|Table2 . id|Table2 . name|
|----|----|----|----|
|1|table1_table2|1|table1_table2|
|none|none|3|table2|

5.使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。
====
* 官方文件關於index的文件：https://dev.mysql.com/doc/refman/5.7/en/optimization-indexes.html
* 其他技術文章： https://ithelp.ithome.com.tw/articles/10221971
1. Optimization and Indexes提到，使用索引的優點是SELECT資料時，可以直接以索引查詢該筆資料所有column的內容。若增加過多不必要的索引，當資料龐大時，會浪費儲存空間與查詢的時間。並不是給個table都需要用到index，需要視需求為該table新增index索引。
2. 基本上它使用的資源如下 :
    * 每個索引都會建立一顆 b+ 樹。
    * 每次新增、更新資料時都會改變 b+ 樹。
3. 索引的使用注意事項：
    1. 連合索引的欄位順序, 例如：{a,b,c}三個欄位，有用到最左邊的欄位的才能使用連合索引。
        ```
        {a, b, c}
        ＝
        {a}
        {a,b}
        {a,b,c}
        SELECT * FROM Table WHERE a = ? ( good 索引 )
        SELECT * FROM Table WHERE a = ? AND b = ? ( good 索引 )
        SELECT * FROM Table WHERE b = ? AND a = ? ( good 索引 )

        SELECT * FROM Table WHERE b = ? ( bad 全掃 )
        SELECT * FROM Table WHERE c = ? ( bad 全掃 )
        SELECT * FROM Table WHERE b = ? AND c = ? ( bad 全掃 )
        ```
    2. 儘可能使用索引的排序, 例如：以年齡為索引，年齡本身就是有排序的。
        ```
        索引欄位: { age }
        SELECT * FROM user WHERE age <= 30 ORDER BY age; ( good 索引 )
        SELECT * FROM user WHERE age <= 30 ORDER BY name; ( bad using filesort )
        ```
    3. 有時太多索引，反而會讓優化器混亂。多化了不少空間建 b+ 樹，而且還會讓 mysql 優化器選錯索引。

6.张三给李四通过网银转账 100 极客币，现有数据库中三张表：
====
请合理设计三张表的字段类型和表结构；
1. 一张为用户表，包含用户 ID 和用户名字
```python
class User_table(Base): 
    __tablename__ = 'user' 
    id = Column(Integer(), primary_key=True, autoincrement=True) 
    name = Column(String(15), nullable=False, unique=True)
```
2. 另一张为用户资产表，包含用户 ID 用户总资产，
```python
class Asset_table(Base): 
    __tablename__ = 'asset' 
    user_id = Column(Integer, ForeignKey('user.id'))
    asset = Column(DECIMAL(19, 4), nullable=True )
```
3. 第三张表为审计用表，记录了 转账时间，转账 id，被转账 id，转账金额。
```python
class transfer_log(Base): 
    __tablename__ = 'transfer_log'
    transfer_time = Column(DateTime(), default = dateime.now() )
    sender_id = Column(Integer, ForeignKey('user.id')) 
    receiver_id = Column(Integer, ForeignKey('user.id')) 
    amount = Column(DECIMAL(19, 4), nullable=False )
```

请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

```Python
# 1. 查詢張三目前帳戶是否有足夠金額
# 2. 減少張三帳戶金額後，增加他人帳戶金額，並記錄到transfer_log的表
# 3. 若張三帳戶金額不足，則顯示金額不足
# 4. 若數據庫crash，

dburl = "mysql+pymysql://testuser:testpass@172.16.129.2:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=False, encoding="utf-8")

SessionClass = sessionmaker(bind=engine)
session = SessionClass()

def deal(session, sender_name, receiver_name, amount):
    #1. 查詢從user與asset兩個表中查詢sender_id與sender_asset
    sender = session.query(User_table).filter(User_table.name == sender_name)
    sender_id = sender.first().id
    sender_asset = session.query(Asset_table).filter(Asset_table.user_id == sender_id)
    
    #2. 若sender_asset不足轉帳amount，則return結果。
    if sender_asset.first().asset < amount:
        return f"{sender.first().name}的帳戶內，不足{amount}。"
    
    try:
    #3. 查詢receiver的id與asset
        receiver = session.query(User_table).filter(User_table.name == sender_name)
        receiver_id = receiver.first().id
        receiver_asset = session.query(Asset_table).filter(Asset_table.user_id == receiver_id)

        sender_asset_after = sender_asset.first().asset - amount
        receiver_asset_after = receiver_asset.first().asset + amount

        sender_asset.update({Asset_table.asset: sender_asset_after})
        receiver_asset.update({Asset_table.asset: receiver_asset_after})

    except:           
        session.rollback()
        raise
    else:
        session.commit()
        return "轉帳成功。"

result = deal('張三', '老皮', 100)
```



