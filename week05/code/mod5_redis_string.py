# 操作string
import redis

client = redis.Redis(host='server1', password='hUN7e4_1')

client.set('key', 'value3', nx=True)

client.append('key', 'value4')
result = client.get('key')

client.set('key2', '100')

result2 = client.incr('key2')  # +1

print(result2)
result3 = client.decr('key2')  # -1
print(result3)

print(result.decode())

# 不要贸然使用keys * 指令,会造成redis短暂不响应
