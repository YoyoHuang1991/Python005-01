# 生产者代码
import pika

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

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = 'send message to fanout'
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message,
                      )

# 关闭与rabbitmq server的连接
connection.close()
