import redis
import time

def check_time(tele, limit=5):
    if client.llen(tele) < limit:
        return True
    time_limit = float(client.lindex(tele, limit-1).decode())
    if (time.time() - time_limit) > 60:
        return True
    else:
        return False


def sendsms(tele: int, content: str, key=None):
    # 短信发送逻辑, 作业中可以使用 print 来代替
    limit = 5
    if check_time(tele, limit):
        now = time.time()
        client.lpush(tele, now)
        print(f"发送成功: {tele}, 內容: {content}, 時間: {time.ctime(now)}")
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    else:
        print(f"發送失敗: {tele}相同手機號碼，一分鐘內最多發送{limit}次，請等待1分鐘")
    

def main():
    sendsms(12345654321, content='hello') # 发送成功
    sendsms(12345654321, content='hello') # 发送成功

    sendsms(88887777666, content='hello') # 发送成功
    sendsms(12345654321, content='hello') # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
    sendsms(88887777666, content='hello') # 发送成功


if __name__ == '__main__':
    client = redis.Redis(host='localhost', password='')
    main()



#期望执行结果：

