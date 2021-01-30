1.在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
====

* 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交 
```Shell
mysql> ALTER DATABASE testdb CHARACTER SET utf8mb4;
```
* 将增加远程用户的 SQL 语句作为作业内容提交
```Shell
mysql> CREATE USER 'testuser'@'%' IDENTIFIED BY 'testpass';
mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%';
```

2.使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
====

* 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
* 将 ORM、插入、查询语句作为作业内容提交