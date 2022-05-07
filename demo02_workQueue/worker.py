# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/6 14:04 
# @description:
import time

import pika

# 建立链接, 若需要链接到远程, 需将 localhost 替换为指定的名称或 IP
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个队列, 可以使用 queue_declare() 方法多次创建同一队列, 但只有一个队列会被真正创建
QUEUE_NAME = 'scrape'
channel.queue_declare(queue=QUEUE_NAME, durable=True)


# 定义一个回调函数, 用于在接收到消息时输出消息
def callback(ch, method, properties, body):
    print(f'message received: {body}')
    time.sleep(body.count('.'.encode()))
    print('message processed')
    ch.basic_ack(delivery_tag=method.deliver_tag)


# 公平调度
channel.basic_qos(prefetch_count=1)
# 定义从哪个队列接收消息
channel.basic_consume(queue='scrape', on_message_callback=callback)
# 处理 I/O 事件和 basic_consume() 回调
channel.start_consuming()
