# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3

from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, Table, Float, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

# 打开数据库连接
# mysql> create database testdb;
# mysql> GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
Base = declarative_base()

class Book_table(Base):
    __tablename__ = 'bookorm'
    book_id = Column(Integer(), primary_key=True)
    book_name = Column(String(50), index=True)

    def __repr__(self):
        return "Book_table(book_id='{self.book_id}', " \
            "book_name={self.book_name})".format(self=self)


class Author_table(Base):
    __tablename__ = 'authororm'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now,
                        onupdate=datetime.now)
# Float 
# Decimal
# Boolean
# Text
# autoincrement 

# 业务逻辑
# 持久层
# 数据库层


# 实例一个引擎
dburl = "mysql+pymysql://testuser:testpass@server1:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")

# 创建session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

# 增加数据
book_demo = Book_table(book_name='肖申克的救赎')
book_demo2 = Book_table(book_name='活着')
book_demo3 = Book_table(book_name='水浒传')
# author_demo = Author_table()
# print(book_demo)
# print(author_demo)

# 增加多条数据
# session.add(book_demo)
# session.add(book_demo2)
# session.add(book_demo3)
# session.flush()

# 使用迭代代替all()
# result = session.query(Book_table).all()
# for result in session.query(Book_table):
#     print(result)

# result = session.query(Book_table).first()
# one() 
# scalar()

# 指定列数
# session.query(Book_table.book_name).first()

# 排序
from sqlalchemy import desc
# for result in session.query(Book_table.book_name, Book_table.book_id).order_by(desc(Book_table.book_id)):
#      print(result)

# 降序
# query = session.query(Book_table).order_by(desc(Book_table.book_id)).limit(3)
# print([result.book_name for result in query])

# 聚合函数
# from sqlalchemy import func
# result = session.query(func.count(Book_table.book_name)).first()
# print(result)

# 条件
# print( session.query(Book_table).filter(Book_table.book_id < 20).first() )
filter(Book_table.book_id > 10, Book_table.book_id <20)

# 连接词
# from sqlalchemy import and_, or_, not_
# filter(
#     or_(
#         Book_table.xxx.between(100, 1000),
#         Book_table.yyy.contains('book')
#     )
# )
session.commit()

