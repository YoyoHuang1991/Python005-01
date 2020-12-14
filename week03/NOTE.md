学习笔记

01 MySQL安裝
====
1. 企業級部屬在linux操作系統，注意版本不同、安裝後避免yum自動更新、數據庫的安全性。
2. CentOS預設用MariaDB，一般我們用MySQL社區版。
3. 可用ssh連現在遠程的linux服務器，
4. 指令arch可查看目前linux是否為64位元系統
5. CentOS，可cat /etc/redhat-release，查看對應版本，使用yum安裝包時，需要先看。
6. 訪問dev.mysql.com，安裝5.7.32的社區版，選擇通用linux版本。先把所有包都下載完成，使用ls -lh可列出文件的大小和具體名字。
7. 先在virtual box 安裝cent OS 7的虛擬機，
	1. http://centos.cs.nctu.edu.tw/7.9.2009/isos/x86_64/
	1. 安裝完成後，設置顯示的字體大小    
		```Shell
		[root@localhost ~]# cd /lib/kbd/consolefonts  //進入到有自體的目錄
		[root@localhost consolefonts]# ls                        //查看所有字體
		[root@localhost consolefonts]# setfont lat4-19                    //設置所選自體，19是字體大小
		[root@localhost consolefonts]# echo 'setfont lat4-16+'  >> /etc/bashrc         //設置為開機時默認字體
		```
	1. 由於是最小安裝，網卡不會隨作業系統開機而開啟，
		```Shell
		//1. 驗證yum 是否正常安裝
		[root@localhost ~]# yum --help 
		//2. 驗證配置resolv.conf:
		[root@localhost ~]# vi /etc/resolv.conf  
		//3. 進入vi編輯模式，按I進入insert添加以下兩行:
		nameserver 8.8.8.8
		search localdomain
		//4. 按Esc，輸入:wq退出vi
		//5. 驗證網卡配置，進入network-scripts找到ifcfg-ens33網卡配置文件
		[root@localhost ~]# cd /etc/sysconfig/network-scripts  
		[root@localhost network-scripts]# ls -a 
		[root@localhost network-scripts]# vi ifcfg-ens33   //若安裝桌面版，檔名可能是ifcfg-enp0s3
		//6. 按I進入insert模式，把onboot的值改為yes, 再按esc後輸入:wq關閉文件
		//7. 重新啟動CentOS
		[root@localhost network-scripts]# reboot
		//8. 驗證yum是否正常運作
		[root@localhost ~]# yum provides ifconfig
		```
1. Yum安裝MySQL（網路上教學）
	1. 安裝MySQL yum repository
	```Shell
	[root@localhost ~]# wget https://repo.mysql.com//mysql57-community-release-el7-11.noarch.rpm
	[root@localhost ~]# yum localinstall mysql57-community-release-el7-11.noarch.rpm
	```

	2. 確認yum repository已安裝
	```Shell
	[root@localhost ~]# yum repolist enabled | grep "mysql.*-community.*"
	```

	3. 查看MySQL發行版本
	```Shell
	[root@localhost ~]# yum repolist all | grep mysql
	```

	4. 安裝MySQL
	```Shell
	[root@localhost ~]# yum install mysql-community-server
	```
	5. 啟動服務與查詢啟動狀態
	```Shell
	[root@localhost ~]# systemctl start mysqld
	[root@localhost ~]# systemctl status mysqld
	```
	6. 查看root初始隨機密碼
	```Shell
	[root@localhost ~]# grep 'temporary password' /var/log/mysqld.log
	```
	7. 修改密碼
	```Shell
	[root@localhost ~]# mysql -uroot -p
	mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassWord!';
	//若跳出錯誤 ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
	//可改用
	set password=password('NewPassWord!');
	```

	8. 遠端連接MySQL設定，外部連接需開啟防火牆MySQL預設3306 Port，檢視3306 Port是否開啟
	```Shell
	[root@localhost ~]# firewall-cmd --query-port=3306/tcp
	no
	```
	目前3306為關閉狀態，需開啟外部才可連接MySQL
	9. 開啟指令
	```Shell
	[root@localhost ~]# firewall-cmd --zone=public --add-port=3306/tcp --permanent
	```
	10. 關閉指令
	```Shell
	[root@localhost ~]#  firewall-cmd --zone=public --remove-port=3306/tcp --permanent
	```
	11. 設定好後重啟防火牆
	```Shell
	[root@localhost ~]# firewall-cmd --reload
	```
	12. 接著修改root用戶可任意IP登入
	```MySQL
	mysql> update mysql.user set host = '%' where user = 'root';
	Query OK, 1 row affected (0.00 sec)
	Rows matched: 1  Changed: 1  Warnings: 0
	```
	13. 最後生效修改命令
	```MySQL
	mysql> flush privileges;
	```
1. yum install（極客大學)
	1. 安裝mysql-community-server，可以直接透過網路更新安裝。若在離線環境安裝，則要下載所需的rpm檔案，再用yum install *.rpm安裝。
	1. 讓MySQL的開發環境與生產環境版本相同，若執行yum update，會把MySQL更新，導致後續版本不同的問題。執行yum remove mysql57-community-release-el7-10.noarch，將下載索引刪除，就不會隨時更新MySQL版本。
	1. MySQL DBA需要特別注意
	1. 啟動MySQL，指令systemctl start mysqld.service，若成功，不會返回值
	1. 讓MySQL隨主機啟動開啟，指令systemctl enable mysqld，若成功，不會返回值
	1. 查詢目前mysql狀態，指令systemctl status mysqld.service，顯示active表示正在運作。
	1. 若安裝mariaDB則無法正常顯示，需執行過濾rpm -qa | grep -i 'mysql'，查看是安裝mariaDB或是MySQL社區版
	1. 若已經啟動多次，要查找安裝MySQL起始密碼，grep 'password' /var/log/mysqld.log | head -1只顯示第一行。
	1. 指令SHOW VARIABLES LIKE 'validate_password%'; 可查看密碼的安全設置。
	1. 指令set global validate_password_policy=0; 降低密碼的安全設置，接著可以設定較簡單的root密碼。
    
02MySQL字符集
====
1. 查看字符集，show variables like '%character%'
2. 查看校對規則，show variables like 'collection_%'
3. Utf8不是utf-8字符集，若變成亂碼，不能修復，學會查看字符集。
4. 也可用navicat字符集管理工具。
5. Linux預設utf8，編輯設定檔，
	```Shell
	vim /etc/my.cnf
	#指令:set nu進入編輯，並輸入以下文字
	[client]
	default_character_set = utf8mb4
	[mysql]
	default_character_set = uft8mb4	
	```
7. [client] default_character_set = uft8mb4，與uft8有何區別？
8. ASCII通常占一個字節，LATIN, GBK微軟內建
9. Utf8最多只能佔3個字節，但emoji或是中文特殊字符都是四個字節，就會報錯。若要不報錯，就得用utf-8,在MySQL裡稱作utf8mb4。若將兩者混用，用戶在輸入特殊字符時就會報錯。
10. 服務端上也有很多配置，依需求調整。以下為較常調整的項目:
	```
	interactive_timeout=28800
	wait_timeout = 288000
	max_connections=1000
	character_set_server = utf8mb4 //這邊要與客戶端統一
	init_connect = 'SET NAMES utf8mb4' //與客戶端連接時，使用該命令
	character_set_client_handshake = FALSE
	collation_server = utf8mb4_unicode_ci
	# 常用以上character_set_server與init_connect設置初始化的字符集。
	```
11. 以上儲存設置完後，並不會生效，需要重啟mysql，便會看到更新後的設置
	```Shell
	[root@localhost ~]# systemctl restart mysqld
	[root@localhost ~]# mysql -u root -p
	mysql> show variables like '%character%'
	```
	1. 第一個設置項character_set_client，客戶端來連的時候使用的字符集
	2. 第二個character_set_connection，連接層面的，建立好三次握手之後
	3. 第三個character_set_database，當前數據庫默認的字符集
	4. filesystem文件系統、results查詢結果的、server默認內部操作、system系統元數據
12. 創建數據庫
	```Shell
	mysql> create database db1 ;   //沒有指定自符集
	mysql> show create database db1; //會顯示已預設utf8mb4創建
	```
13. 更新的時候，字符集會先以client再以connection、database這樣的順序字符集。查詢的時候，會先以表的字符集，再以character_set_results。
14. collate是表的校對規則，
	```Shell
	mysql> show variables like 'collation_%';   
	//顯示默認皆為utf8mb4_unicode_ci，_ci表示大小寫不敏感，_cs表示大小寫敏感。
	```
	
03多種方式連接MySQL數據庫
====
1. 連接方式，其他語言稱「連接器、綁定、binding」，Python稱「Python database API、DB-API」，MySQLdb是Python2，適用MYSQL5.5和Python2.7，不要對老系統做升級。
2. Python3之裝MySQLdb包叫做mysqlclient，
	```Shell
	shell> pip install mysqlclient
	python> import MySQLdb
	```
3. 其他DB-API，需要手動拼接SQL:
	```Shell
	pip install pymysql   #流行度最高
	pip install mysql-connector-python #MySQL官方
	```
4. 使用ORM(Object Relational Mapping)，Django web也集成使用的方法。對原始的DB-API的擴充，需要先import 前邊的DB-API，為更高級的封裝
	```Shell
	pip install sqlalchemy
	```
5. 打開mod3_pymysql_conn.py。
6. 打開mod3_sqlalchemycore_conn.py
	1. create_engine中echo=True是開發環境調式用。
	2. 創建元數據，例如一本圖書，頁數、標題、作者、分類，先對數據做初始化。
7. 回到mysql主機，查看新增的db
	```Shell
	mysql> use testdb;
	mysql> show tables;
	mysql> show create table book;
	mysql> show create table author;
	```
8.轉變成ORM的方式，打開mod3_orm_conn.py，使用ORM必須滿足的四個要求。
	1.創建base必須繼承自declarative_base()
	2.創建表時，可用class做指定，__tablename，必須用雙下畫線
	3.包含一個或多個屬性column
	4.必須要有一個主鍵primary_key
	5.使用ORM當客戶要求增加新屬性時，直接在class中新增即可，產生錯誤較低。
	6.規範寫法中，import要寫在最上面。
	7.created_on創建時間，updated_on更新時間
	8.dburl這裡指定字符集，避免設定字符出錯，?charset=utf8mb4；
	9.create_enging連接時用utf-8
	10.Base.metadata.create_all(engine)對於引擎進行執行
9.回到mysql
	```Shell
	mysql> show tables;
	mysql> show create table authororm ;
	//列出ORM如何創建table
	```

04必要的ＳＱＬ知識
====
1. 功能劃分：
	1. DQL, 數據查詢語言，開發工程師學習的重點
	2. DDL, 數據定義語言 ，庫和表結構
	3. DML, 操作表中紀錄 
	4. DCL, 控制語言，安全和訪問權限控制
2. 創建表之前，要確認表是否存在，否則會報錯。使用反引號，因為名稱有可能出現單引號，故以此作區別，與ＭySQL保留字段作區別。不用儲存emoji表情，所以使用utf8。
3. 創建數據表的個數，愈少愈好，簡潔愈好。字段愈少愈好，相互獨立。字段的值不建議是由其他字段計算出，會增加冗余和降低檢索效率。
4. 表聯合主鍵的字段也是愈少愈好，聯合主鍵愈多，索引查詢運行的時間愈大。
5. 外鍵應該用嗎？如果對內部系統，只需關注正確性可用外鍵；若外部，則是在應用層解決，許多大廠，不允許外鍵在內部系統用，否則會造成內容更新的阻塞。要求正確性大於性能，可用外鍵，若是併發系統，外鍵要通過應用的業務層和邏輯層做解決。
6. 如何進行查詢？
	1. SELECT查詢時關鍵字順序
	2. SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT
		i. 生產環境下因為列數相對較多，一般禁用SELECT
		ii. ＷHERE字段為避免全表掃描，一般需增加索引。
	3. 執行順序是FROM>WHERE
7. 打開table.sql
	1. SELECT DISTUNCT book_id, book_name, count(*) as number  #5
	2. FROM book JOIN author ON book.sn_id = author.sn_id   #1執行順序，產生新的虛擬表
	3. WHERE pages > 500                ＃2執行順序
	4. GROUP BY book.book_id        ＃3排序 
	5. HAVING number > 10             ＃4 輸大於10
	6. ORDER BY number                    #6
	7. LIMIT 5                    #7取前五個

05使用聚合函數匯總數據
====
1. SQL函數有哪些？算數、字符串、日期、轉換、聚合（匯總表的數據）
2. 聚合函數：COUNT()行數、MAX()最大值、MIN()最小值、SUM()求和、AVG()平均值
3. 輸入的是一組數據的集合，輸出單個值，忽略空行
4. 打開mysql，打開db1範例數據庫
```Shell
mysql> show databases
mysql> user db1 ; 
mysql> select * from t1 limit 5 \G

```
5. id 是自增的主鍵，short 評等，n_star星級
```Shell
mysql> select count(*) from t1 ;   #可查詢總共有570條紀錄，可能包含空值
select count(*), avg(n_star), max(n_star) from t1 where id < 10 ;   #多少條，平均星級，最大星級是多少
```
6. 用group by 看每個星級的數量
```shell
mysql> SELECT count(*) , n_star from t1 group by n_star
```
7. Where增加過濾，Group by 進行分組，分組後也可以過濾，但要改用having。Ｗhere過濾指作用於每一行，having則作用於分組。
```shell
mysql> selec count(*), n_star from t1 group by n_star having n_star > 3 order by n_star DESC;
```
8. Count(*)會忽略空行，要特別注意。

06多表操作用到的子查詢和join關鍵字解析
====
1. 須從查詢結果集中再次進行查詢，才能得到想要的結果。猶如for循環
非關聯，for裡面沒有for：關聯子查詢，for裡面有for。
```Shell
mysql> select count(*) , n_star from t1 group by n_star having n_star > 3 order by n_star desc;  
#使用平均星級查詢，條件嵌套，裡面的只做一次，稱為非關聯子查詢
mysql> SELECT avf(n_star) from t1; 
mysql> SELECT COUNT(*), n_star FROM t1 GROUP BY n_star HAVING n_star > (SELECT avg(n_star) FROM t1) ORDER BY n_star DESC ; 

```
2. 關聯子查詢，通常特過DBA執行，常用EXIT IN 小表驅動大表。
```Shell
mysql> TABLE_A TABLE_B \c
mysql> SELECT * FROM TABLE_A WHERE condition IN (SELECT condition FROM TABLE_B) \c
mysql> SELECT * FROM TABLE_A WHERE EXIT (SELECT condition FROM B WHERE B.condition=A.condition) \c
```
轉成python，如下邏輯：
```Python
for I in TABLE_B:
	for j in TABLE_A:
		if TABLE_B.condition == TABLE_A.condition:
			…

```
3. 常用JOIN聯集有哪些？前三種較常用
	1. INNER JOIN
	2. LEFT JOIN
	3. RIGHT JOIN
	4. FULL OUTER JOIN，對mysql並不支持，若要用則用UNION
	5. ….

07事務的特性和隔離級別
====
1. 事務：要麼全執行，要麼不執行，例如：購物流程中最關鍵的是，是否付款，是否清空購物車。
2. 事務的特性ACID
	1. 原子性（不可分割）atomicity
	2. 一致性consistency
	3. 隔離性isolation
	4. 持久性durability
3. 事務隔離級別SQL92的標準
	1. 讀未提交：允許讀到未提交的數據 //當ＡＢ兩個事務，在操作同一個內容時，Ａ可以讀到Ｂ尚未提交的內容；Ａ讀取到一半，Ｂ退回，Ａ會讀到無意義的中間內容。
	2. 讀已提交：只能讀到已經提交的內容 //事務Ｂ已完成，事務Ａ才有辦法讀到。
	3. 可重複讀：同一事物在相同查詢條件下兩次查詢得到的數據結果一致   //常與讀已提交混淆，兩次查詢間，內容已被更改，所以兩次結果會不同。若要相同條件，查詢內容皆一致，則要設為可重複讀。
	4. 可串行化：事務進行串行化，但是犧牲了併發性能
4. 數據是自動提交的，如何控制是否自動提交？默認自動提交，專業術語稱『隱式提交』，若為oracle的資料庫則默認需要手動提交。
```Shell
mysql> show variables like 'autocommit';
mysql> set autocommit=0 ;
mysql> show variables like 'autocommit' ;
```
5. 手動提交，若要開啟一個事務，則以BEGIN開始，COMMIT結束。
6. 假設清空購物車後要做付款時，取消付款，則要做回滾ROLLBACK，回到BEGIN狀態。
7. 一個事務可以有多個保存點，用ROLLBACK回到保存點。
8. 隔離級別愈低，產生異常愈多。讀未提交，級別低，但更有效共享資源。

08PyMySQL的增刪改查操作演示
====
1. 開啟mod3_pymysql_conn.py，一般查詢都要遵循的四個步驟
	1. 導入第三方庫import pymysql
	2. 建立連接pymysql.connect() 配置項目通常會另外寫配置文件內
	3. 執行sql語句，使用with會自行關閉數據庫，若用open，則要記得cursor.close()
	4. 關閉數據庫
2. 打開mod3_pymysql_insert.py，插入
	1. 建立連接後，執行insert，value用%s插入指定字段，這裡無論是否為數字都是%s佔位符。sql語句可以用單引號或是三引號的方式。
	2. 用.excute()將sql與value語句做拼接。直到執行db.commit()之後，才會將數據寫進去。
	3. 雖然mysql預設隱式提交，但使用pymysql時，是顯式提交。若用SQLalchemy則不需要手動commit()，已經寫成隱式提交。
	4. print(cursor.rowcount) 非表中有多少行數，而是現在輸入幾行資料到數據庫。
	5. 進到mysql查看輸入的狀況

	```Shell
	mysql> select * from book ;
	//可看到數據庫有哪些紀錄
	```
3. 打開mod3_pymysql_query.py，查詢功能：
	1. cursor.fetchall()取出匹配的所有行，取出來是元祖tuple類型。
	2. .fetchone()取出一行，結果集當中的一行
4. 打開mod3_pymysql_update.py，更新功能：
	1. 依照sql語句的邏輯，應該將id與where的位置調換，才會更新成功。
5. 打開mod3_pymysql_delete.py，刪除功能：
	1. 用cursor.rowcount返回值的方式，確認數據庫操作是否成功，並且結果是否符合預期。

09多文件插入＆如何設計一個良好的數據庫連接配置文件
====
1. 打開mod3_pymysql_insertmany.py，
	1. 用tuple嵌套的方式將兩筆value總成一個values，使用cursor.excutemany(sql, values)
	2. 將server設置提取出來，需考慮Unix或linux設計的思維，linux會將用戶名與密碼放在/etc/passwd的文件中，根據文件的固定格式，分割出不同字段。
	3. 存放mysql配置文件
	4. 若配置要連接網路設置多個節點，則不會將配置存放到文件中。
	5. 目前流行ini格式儲存配置文件，其他有yaml或json格式。打開config.ini
	6. 如何設計前邊固定的名稱？可參考pymysql.connect()對應的參數，來設定ini配置的變數名稱，意義更明確，順序也可以發生變化。
		i. 配置文件可讀性
		ii. 簡單明確，直到要填寫得內容
		iii. 配置之所以存到文件，是為了文件型的儲存更加穩定，若要給集群或多機使用，要使用一些配置的數據庫服務器。經常在微服務看到配置服務。
		iv. 用關鍵字讀取名字，而不是直接按照順序寫入
2. 打開dbconnect.py
	1. 通過字典dict()的形式，將配置讀入connect()。
	2. 打開dbconfig.py
	3. 其中用ConfigParser()將filename讀取，再用.items(section) 抓[mysql]底下的內容為list()，其中是包含許多tuple，所以要用dict()轉為字典的形式。

10使用SQLAlchemy插入數據到ＭySQL數據庫
====
1. 打開mode3_orm_insert.py
2. 方便查看的模式方法__repr__
3. ＯＲＭ三層結構，
	1. 業務邏輯層：抽象話，就不須關心數據庫層。直接編輯需要哪些表就好。
	2. 持久層：對數據庫更高效的訪問，SQLalchemy完成ORM
	3. 數據庫層：通過持久層映射到業務層
4. 缺點是需要實體化表，session轉化成SQL語言，其過程也會造成性能的損耗。優點是關心業務層，與底層分開。缺點，抽象並不能覆蓋所有底層功能。複雜的查詢還是得回到原始的SQL。
5. 跟DBA打交道，需要用SQL溝通。
6. Django使用MTV架構，model模型也是一個ORM，Django用model與數據庫操作。
7. 列的類型Float Decimal Boolean Text, autoincrement（自動增長），使用前記得import相應的數據庫
8. 約束 primary, nullable, default, 
9. 創建session（會話），底層架構是確認對象的表和主鍵。自己還維護一個事務，一直保持打開的狀態，一直到會話提交或是回滾。
10. sessionmaker是一個工廠模式，先記成是一個固定的書寫模式 。將session=SessionClass()理解為開始一個事務。

11使用SQLAlchemy查詢MySQL(上)
====
1. 打開mod3_orm_insert.py，查詢操作直接更換sesson.add(book_demo)的add部分。
2. 除了commit()，也有flush()但當前的事務會繼續保持連接，並沒有被寫入數據庫。使用flush()後，還是要用commit()。
3. 查詢用session.query(book_table)，只執行這個僅返回空的，要用session.query(book_table).all()，才會返回所有結果。將結果附值到變數result中，再print(result)。
4. 獲取其中一個值，把.all()改成.first()。
5. 用迭代而非all的方式，for result in session.query(Book_table): print(result)
6. 除了first()，另有兩個相似的function。one() 查詢所有行，如果結果不是單獨一個，就會異常；schalar()返回第一個結果的第一個元素，要確保資料庫只有一行，才能用，否則常會顯示異常。
7. 控制指定列數，session.query(book_table.book_name),first()，指定查詢表中book_name那一列。
8. 排序，
```Python
from sqlalchemy import desc
for result in session.query(Book_table.book_name, Book_table.book_id).order_by(desc(Book_table.book_id)): 
	print(result)
```
9. 排序、限制返回結果
```Python
query = session.query(Book_table).order_by(desc(Book_table.book_id)).limit(3)
print([result.book_name for result in query])
```

12使用SQLAlchemy查詢MySQL(下)
====
1. 聚合函數多行彙總
```Python
from sqlalchemy import func
result = session.query(func.count(Book_table.book_name)).first()
print(result)   #獲得一個元祖tuple
session.commit()
```
2. filter語句(SQL中的where)，
```Python
print(session.query(Book_table).filter(Book_table.book_id < 20).first())
```
3. 更複雜的形式
```Python
filter(Book_table.book_id > 10, Book_table.book_id < 20)
from sqlalchemy import and_, or_, not_    #若沒有用_，可能會跟其他functionr衝突，用到甚麼，就import甚麼。
filter(
	or_(
		Book_table.xxx.between(100, 1000), 
		Book_table.yyy.contains('book')
	)
)
session.commit()
```

13使用SQLAlchemy更新和刪除MySQL
====
1. 更新用update()，
```Python
query = session.query(Book_table)
query.filter(Book_table.book_id == 20)
query.update({Book_table.book_name: 'newbook'})
new_book = query.first()
print(new_book.book_name)

```
2. 刪除數據delete()，不接收參數
```Python
query = session.query(Book_table)
query.filter(Book_table.book_id == 19)
session.delete(query.one()) 

#就地刪除，不用查詢再刪除的方法
query = session.query(Book_table)
query.filter(Book_table.book_id == 18)
query.delete()
print(query.first())
```

```mysql
mysql> select * from bookorm;  //查看刪除的結果
```
	
14使用連結池&數據庫建立連接的過程
====
1. 打開mod3_conn_pool.py，引用pip3 install DBUtils
```Python
from dbutils.pooled_db import PooledDB  #多線程數據連接，就要用這樣一個包

```
2. PooledDB()封裝了之前用的connect()，可看他是如何封裝先前的功能
3. 關鍵參數可用dict()命名，再用**db_config將內容導入
4. 最大連接池限制，節省效能
5. 創建空閒連接，時間換空間，初始連接直接創建空閒，客戶端TCP建立連接後在內存空間保存已經建立連接的狀態，服務端占用更多描述符。
6. 最多空閒連接，釋放掉峰值之後產生過多的連接
7. 重複使用的次數，避免內存洩漏，如果多次使用，內存無法釋放。線程銷毀，再重新建立。
8. 沒有連接可用時，是否進行阻塞。
	1. True等待，盡可能讓用戶請求成功；False不等待然後報錯
9. 根據硬件配置，做連接數大小的設置
10. spool = PooledDB()，後續用法是跟先前相同的，只是連接前先做設置。

15優化數據庫使用的基本原則
====
1. 調優不是萬能，依據業務需求作調優，提升硬件配置，而不是壓榨性能
	1. CPU
	2. 內存
	3. 網路連接
2. 第一次效果最明顯
3. 有體系調整，不是發現一個參數可以調就試一試
4. 打開阿里巴巴Java的開發手冊
	1. 參考開發手冊，找到符合業務需求的規則，需要完整看規約與準則。
	2. 增加監控系統，當業務遇到瓶頸時，再做調優。

本周作業
====
1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
	将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
	将增加远程用户的 SQL 语句作为作业内容提交

2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
	用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
	将 ORM、插入、查询语句作为作业内容提交
3. 为以下 sql 语句标注执行顺序：
```
SELECT DISTINCT player_id, player_name, count(*) as num 
FROM player JOIN team ON player.team_id = team.team_id 
WHERE height > 1.80 
GROUP BY player.team_id 
HAVING num > 2 
ORDER BY num DESC 
LIMIT 2
```
4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

	Table1

	id name

	1 table1_table2

	2 table1

	Table2

	id name

	1 table1_table2

	3 table2

	举例: INNER JOIN

	```
	SELECT Table1.id, Table1.name, Table2.id, Table2.name
	FROM Table1
	INNER JOIN Table2
	ON Table1.id = Table2.id;
	```
5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：
	一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
	第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

	请合理设计三张表的字段类型和表结构；
	请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
	
	

