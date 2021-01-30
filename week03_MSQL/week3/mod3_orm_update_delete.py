# ORM方式连接 MySQL 数据库
# pip3 install sqlalchemy
#!/usr/bin/python3

from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, desc, Table, Float, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()

class Book_table(Base):
    __tablename__ = 'bookorm'
    book_id = Column(Integer(), primary_key=True)
    book_name = Column(String(50), index=True)

    def __repr__(self):
        return "Book_table(book_id='{self.book_id}', " \
            "book_name={self.book_name})".format(self=self)

# 实例一个引擎
dburl = "mysql+pymysql://testuser:testpass@server1:3306/testdb?charset=utf8mb4"
engine = create_engine(dburl, echo=True, encoding="utf-8")

# 创建session
SessionClass = sessionmaker(bind=engine)
session = SessionClass()


# 更新
query = session.query(Book_table)
query = query.filter(Book_table.book_id == 20)
query.update({Book_table.book_name: 'newbook'})
new_book = query.first()
print(new_book.book_name)

# 删除
query = session.query(Book_table)
query = query.filter(Book_table.book_id == 18)
# session.delete(query.one())
query.delete()
print(query.first())



session.commit()

