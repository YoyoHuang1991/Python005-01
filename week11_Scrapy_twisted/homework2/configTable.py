"""
1. table欄位(6)：id, city, salary, position, company_name, created_date，各取100筆
2. 相同city, salary, position時，去除重複。
3. city分為台北、新北市、台中、高雄
"""
import pymysql
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime 
from sqlalchemy import DateTime

Base = declarative_base()

class Job_table(Base): 
    __tablename__ = 'job_table' 
    job_id = Column(Integer(), primary_key=True) 
    job_city = Column(String(15), nullable=False)
    job_salary = Column(Integer())
    job_position = Column(String(15), nullable=False)
    job_company = Column(String(15), nullable=False)
    created_date = Column(DateTime())

    def __repr__(self):
        ret = f"工作地區：{self.job_city} \n薪資：{self.job_salary}\n職位：{self.job_position}\n公司：{self.job_company}\n{self.created_date}\n============\n"

        return ret

dburl="mysql+pymysql://yuyu:1234@10.225.109.101:3306/homework2?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)