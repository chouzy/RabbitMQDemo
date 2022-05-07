# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/6 14:00 
# @description:
import sys

import pika

# 建立链接, 若需要链接到远程, 需将 localhost 替换为指定的名称或 IP
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个队列
QUEUE_NAME = 'scrape'
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# 发送消息到队列
message = ' '.join(sys.argv[1:]) or 'hello world'
channel.basic_publish(exchange='', routing_key='scrape', body=message, properties=pika.BasicProperties(delivery_mode=2))
print(f'message sent: {message}')

# 退出程序, 关闭链接
connection.close()
