# 连接 Redis
import redis
# pip3 install redis

client = redis.Redis(host='192.168.56.101', password='testpass')

print(client.keys())

for key in client.keys():
    print(key.decode())
