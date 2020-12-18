# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3
 
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# 打开数据库连接
# mysql> create database testdb;
# mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';

Base = declarative_base()

class Book_table(Base): 
    __tablename__ = 'bookorm' 
    book_id = Column(Integer(), primary_key=True) 
    book_name = Column(String(50), index=True) 


# book_table=Table('book',metadata,
#     Column('id',Integer,primary_key=True),
#     Column('name',String(20)),
#     )

# 定义一个更多的列属性的类
# 规范写法要记得写在最上面
from datetime import datetime 
from sqlalchemy import DateTime

class Author_table(Base): 
    __tablename__ = 'authororm' 
    user_id = Column(Integer(), primary_key=True) 
    username = Column(String(15), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now) 
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# 实例一个引擎
dburl="mysql+pymysql://testuser:testpass@server1:3306/testdb?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)
