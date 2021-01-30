# 操作list
import redis
import time

client = redis.Redis(host='localhost', password='')

# 存入列表
client.lpush('list_redis_demo', time.time())
client.lpush('list_redis_demo', time.time()+10)
# client.rpush('list_redis_demo', 'java')
# data = client.lpop('list_redis_demo')
# 查看长度
print(client.llen('list_redis_demo'))

# 弹出数据
# lpop() rpop()
# data = client.lpop('list_redis_demo')
# print(data)

# 查看一定范围的list数据
# data = client.lrange('list_redis_demo', 0, -1)
# print(data)

# while True:
#     phone = client.rpop('list_redis_demo')
#     if not phone:
#         print('发送完毕')
#         break

    # sendsms(phone)
    # result_times = retry_once(phone)
    # if result_times >= 5:
    #     client.lpush('list_redis_demo', phone)

# data = client.lrange('list_redis_demo', 0, 1)
index0 = float(client.lindex('list_redis_demo', 0).decode())
index4 = float(client.lindex('list_redis_demo', 1).decode())
print(f"{time.ctime(index0)} - {time.ctime(index4)} = {index0 - index4}")