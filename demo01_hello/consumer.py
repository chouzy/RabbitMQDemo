# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/6 10:08
# @description:
import pika

# 建立链接, 若需要链接到远程, 需将 localhost 替换为指定的名称或 IP
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个队列, 可以使用 queue_declare() 方法多次创建同一队列, 但只有一个队列会被真正创建
QUEUE_NAME = 'scrape'
channel.queue_declare(queue=QUEUE_NAME)


# 定义一个回调函数, 用于在接收到消息时输出消息
def callback(ch, method, properties, body):
    print(f'Get {body}')


# 定义从哪个队列接收消息
channel.basic_consume(queue='scrape', auto_ack=True,
                      on_message_callback=callback)
# 处理 I/O 事件和 basic_consume() 回调
channel.start_consuming()
