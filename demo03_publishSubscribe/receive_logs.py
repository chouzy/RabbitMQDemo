# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/6 16:46 
# @description:
import pika

# 建立链接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 定义环形交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 创建新的随机队列
result = channel.queue_declare(exclusive=True, queue='')
# 获取新创建的随机队列的队列名
queue_name = result.method.queue  # amq.gen-EPUv8ZL0_5-d0I1TiFJSuw
# 绑定交换机和队列
channel.queue_bind(exchange='logs', queue=queue_name)


# 定义回调方法
def callback(ch, method, properties, body):
    print(f'message is:{body}')


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
channel.start_consuming()
