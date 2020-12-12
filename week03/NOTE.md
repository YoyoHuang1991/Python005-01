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
5. Linux預設utf8，編輯設定檔，指令:set nu進入編輯
	```Shell
	vim /etc/my.cnf
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
	

	
	
	

