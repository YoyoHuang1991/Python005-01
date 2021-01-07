# 操作hash
import redis

client = redis.Redis(host='192.168.56.101', password='testpass')

# client.hset('vip_user', '1001', 1)
# client.hset('vip_user', '1002', 1)
# client.hdel('vip_user', '1002')
# print(client.hexists('vip_user','1001'))

# 添加多个键值对
# client.hmset('vip_user', {'1003':1, '1004':1})
client.hset('vip_user', mapping={'1003':100, '1004':1}) #hmset要逐漸被淘汰
# hkeys hget hmget hgetall
# field = client.hkeys('vip_user') #以list輸出
# print(field) 
print(client.hget('vip_user', '1003'))
# print(client.hgetall('vip_user'))
# bytes
