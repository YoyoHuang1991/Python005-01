import pymysql
from dbconfig import read_db_config

dbserver = read_db_config()
db = pymysql.connect(**dbserver)

try:

    # 使用 cursor() 方法创建一个游标对象 cursor
    with db.cursor() as cursor:
        sql = '''SELECT VERSION()'''
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute(sql)
        result = cursor.fetchone()
    db.commit()

except Exception as e:
    print(f"fetch error {e}")

finally: 
    # 关闭数据库连接
    db.close()

 
print (f"Database version : {result} ")

