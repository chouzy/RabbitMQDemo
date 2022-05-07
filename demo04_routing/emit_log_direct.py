# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/7 9:36 
# @description:
import sys

import pika

# 建立链接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 创建直连交换机
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
# 发送消息
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'hello world'
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print(f'message is: {message}')
# 关闭链接
connection.close()
