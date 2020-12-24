作业一：使用 Python+redis 实现高并发的计数器功能
====
1. 需求描述:
在社交类网站中，经常需要对文章、视频等元素进行计数统计功能，热点文章和视频多为高并发请求，因此采用 redis 做为文章阅读、视频播放的计数器。
请实现以下函数：

```Python
counter()
def counter(video_id: int):
    ...
    return count_number
```

2. 函数说明:
counter 函数为统计视频播放次数的函数，每调用一次，播放次数 +1
参数 video_id 每个视频的 id，全局唯一
基于 redis 实现自增操作，确保线程安全
期望执行结果：
conuter(1001) # 返回 1
conuter(1001) # 返回 2
conuter(1002) # 返回 1
conuter(1001) # 返回 3
conuter(1002) # 返回 2
…

3. 选做:：
可以基于 Django+ redis 实现，使用 redis 作为 Django 后端可参考如下代码：
https://django-redis-chs.readthedocs.io/zh_CN/latest/

作业二：在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口：
====
1. 已知有如下函数：
```python
def sendsms(telephone_number: int, content: string, key=None)：
    # 短信发送逻辑, 作业中可以使用 print 来代替
    pass
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    pass
    print("发送成功")

#期望执行结果：

sendsms(12345654321, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 发送成功

sendsms(88887777666, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
sendsms(88887777666, content=“hello”) # 发送成功
```

2. 选做：
    1. content 为短信内容，超过 70 个字自动拆分成两条发送
    2. 为 sendsms() 函数增加装饰器 send_times()，通过装饰器方式实现限制手机号最多发送次数，如：
    ```python
    @send_times(times=5)
    sendsms()
    ```
作业三：请用自己的语言描述如下问题：
====
1. 在你目前的工作场景中，哪个业务适合使用 rabbitmq？ 引入 rabbitmq 主要解决什么问题?（非相关工作可以以设计淘宝购物和结账功能为例来描述）
2. 如何避免消息重复投递或重复消费？
3. 交换机 fanout、direct、topic 有什么区别？
4. 架构中引入消息队列是否利大于弊？你认为消息队列有哪些缺点？
5. 作业 3 提示：
    1. 服务间异步通信
    2. 顺序消费
    3. 定时任务
    4. 流量削峰
    5. 解耦
    6. 利用消息队列将高并发访问变为串行操作
    7. 异步下单
    8. 消息队列持久化