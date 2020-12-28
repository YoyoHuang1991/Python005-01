# 消费者代码
import pika

credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明消息队列
channel.queue_declare(queue='direct_demo', durable=False)

# 定义一个回调函数来处理消息队列中的消息
def callback(ch, method, properties, body):

    # 手动发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # 实现如何处理消息
    print(body.decode())

# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume('direct_demo',on_message_callback=callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()
