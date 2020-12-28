# 生产者代码
import pika
# pip3 install pika

# 用户名和密码
credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
# 阻塞方法
connection = pika.BlockingConnection(parameters)

# 建立信道
channel = connection.channel()

# 声明消息队列
# 如不存在自动创建
# durable=True 队列持久化
channel.queue_declare(queue='direct_demo', durable=False)

# exchange指定交换机
# routing_key指定队列名
channel.basic_publish(exchange='', routing_key='direct_demo',
                      body='send message to rabbitmq')

# 关闭与rabbitmq server的连接
connection.close()
