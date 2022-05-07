# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/5/7 11:41
# @description:
import uuid

import pika


class FibonacciRpcClient(object):
    def __init__(self):
        """ 初始化，建立链接 """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True, queue='')
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        """ 回调函数，检测响应的 correlation_id 是否符合预期 """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        """ 执行 RPC 请求 """
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id), body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
print(f'Requesting fib(30)')
response = fibonacci_rpc.call(30)
print(f'Got {response}')
