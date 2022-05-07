# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/7 10:27 
# @description:
import sys

import pika

# 建立链接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 定义环形交换机
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 创建队列
result = channel.queue_declare(exclusive=True, queue='')
queue_name = result.method.queue

# 绑定队列
binding_keys = sys.argv[1:]
if not binding_keys:
    print(sys.stderr)
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)


# 回调函数
def callback(ch, method, properties, body):
    print(f'routing_key is: {method.routing_key}, message is: {body}')


# 接收队列消息
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
