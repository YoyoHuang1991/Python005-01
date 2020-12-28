# 操作set
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

print(client.sadd('redis_set_demo', 'new_data'))
# client.spop()
# client.smembers('redis_set_demo')

# 交集
client.sinter('set_a', 'set_b')

# 并集
client.sunion('set_a', 'set_b')

# 差集
client.sdiff('set_a', 'set_b')