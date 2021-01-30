import redis

def counter(video_id: int):
    return client.incr(video_id)


client = redis.Redis(host='localhost', password='')

video = {
    '1001':0,
    '1002':0
    }
client.hset('video_id', mapping=video)


print(counter(1001)) # 返回 1
print(counter(1001)) # 返回 2
print(counter(1002)) # 返回 1
print(counter(1001)) # 返回 3
print(counter(1002)) # 返回 2