# 操作list
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

# 存入列表
# client.lpush('list_redis_demo', 'python')
# client.rpush('list_redis_demo', 'java')

# 查看长度
print(client.llen('list_redis_demo'))

# 弹出数据
# lpop() rpop()
# data = client.lpop('list_redis_demo')
# print(data)

# 查看一定范围的list数据
# data = client.lrange('list_redis_demo', 0, -1)
# print(data)

while True:
    phone = client.rpop('list_redis_demo')
    if not phone:
        print('发送完毕')
        break

    # sendsms(phone)
    # result_times = retry_once(phone)
    # if result_times >= 5:
    #     client.lpush('list_redis_demo', phone)

data = client.lrange('list_redis_demo', 0, -1)
print(data)