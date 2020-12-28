# 操作zset
import redis
import time

client = redis.Redis(host='server1', password='hUN7e4_1')

client.set('newkey', 'value')
client.expire('newkey', 3)
print(client.exists('newkey'))

# 休眠5秒
time.sleep(2)
# 过期是个时间偏移量,单位秒
# client.expire('newkey', 3)
# time.sleep(2)
print(client.exists('newkey'))
print(client.ttl('newkey'))