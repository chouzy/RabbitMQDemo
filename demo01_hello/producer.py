import pika

# 建立链接, 若需要链接到远程, 需将 localhost 替换为指定的名称或 IP
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个队列
QUEUE_NAME = 'scrape'
channel.queue_declare(queue=QUEUE_NAME)

# 发送消息到队列
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='hello world')

# 退出程序, 关闭链接
connection.close()