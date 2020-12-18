# sqlalchemy 连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3
 
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey

# 打开数据库连接
# mysql> create database testdb;
# mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
# echo=True 开启调试
engine=create_engine("mysql+pymysql://testuser:testpass@server1:3306/testdb",echo=True)
 
# 创建元数据
metadata=MetaData(engine)
 
book_table=Table('book',metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String(20)),
    )
author_table = Table('author', metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', None, ForeignKey('book.id')),
    Column('author_name', String(128), nullable=False)
    )

try:
    metadata.create_all()
except Exception as e:
    print(f"create error {e}")
 
