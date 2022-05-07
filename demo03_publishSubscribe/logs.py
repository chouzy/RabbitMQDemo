# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/6 16:13 
# @description:
import sys

import pika

# 建立链接
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 定义环形交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 发送消息并指定使用环形交换机
message = ' '.join(sys.argv[1:]) or 'info: hello world'
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f'message is: {message}')
# 关闭链接
connection.close()
