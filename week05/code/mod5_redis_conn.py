# 连接 Redis
import redis
# pip3 install redis

client = redis.Redis(host='server1', password='hUN7e4_1')

print(client.keys())

for key in client.keys():
    print(key.decode())
