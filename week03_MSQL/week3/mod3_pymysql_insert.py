#!/usr/bin/python3 
import pymysql
 
db = pymysql.connect("server1","testuser","testpass","testdb")
 
try:

    # %s是占位符
    with db.cursor() as cursor:
        sql = 'INSERT INTO book (id, name) VALUES (%s, %s)'
        value = (1002, "活着")
        cursor.execute(sql, value)
    db.commit()

except Exception as e:
    print(f"insert error {e}")

finally: 
    # 关闭数据库连接
    db.close()
    print(cursor.rowcount)

