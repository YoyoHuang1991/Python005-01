# 消费者代码
import pika
import time

credentials = pika.PlainCredentials('guest', 'hUN7e4_1')

parameters = pika.ConnectionParameters(host='server1',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明消息队列
channel.queue_declare(queue='task_queue', durable=True)

# 定义一个回调函数来处理消息队列中的消息


def callback(ch, method, properties, body):


    time.sleep(1)
    print(body.decode())
    # 手动确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 如果该消费者的channel上未确认的消息数达到了prefetch_count数，则不向该消费者发送消息
channel.basic_qos(prefetch_count=1)

# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume('task_queue', callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()
