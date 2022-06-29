import pika
from cspider_info.env_setting import *


def get_error_mes(package_type,msg_type):
    # credentials = pika.PlainCredentials('mickey', 'qwer123wasd')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '39.107.36.205')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'mickey')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'qwer123wasd')
    RABBITMQ_CONNECTION_PARAMETERS = \
        os.getenv('RABBITMQ_CONNECTION_PARAMETERS',
                  f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}')

    params = pika.URLParameters(f'{RABBITMQ_CONNECTION_PARAMETERS}/{package_type}_vhost?heartbeat=0')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
    # channel.queue_declare(queue='python-test1', durable=False)

    # 创建临时队列，队列名传空字符，consumer关闭后，队列自动删除
    # channel.queue_declare(f'{package_type}_{msg_type}', exclusive=True)
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange='direct_test_exchange', durable=True, exchange_type='direct')
    # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
    channel.queue_bind(exchange=f'{package_type}_exchange', queue=f'{package_type}_{msg_type}_queue', routing_key=f'{package_type}_{msg_type}_route')


    # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
    def callback(ch, method, properties, body):
        # print(body.decode())
        package_name = body.decode('utf-8')
        print(str(package_name))
        with open('error_mes.txt', 'w', encoding='utf-8') as f:
            f.writelines(str(package_name))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # 告诉rabbitmq，用callback来接收消息
    # channel.basic_consume('python-test3', callback)

    # 告诉rabbitmq，用callback来接受消息
    channel.basic_consume(f'{package_type}_{msg_type}_queue', callback,
                          # 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
                          auto_ack=False)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()

# # 调用common_methods中的方法输出队列消息
# def putout_error_mes(channel, method, header_props, message):
#         while True:
#             # print(message)
#             package_name = message.decode('utf-8')
#             print("package_url = "+package_name)
#             with open('error_mes.txt', 'w', encoding='utf-8') as f:
#                 f.writelines(package_name)
#             channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    # consuming_message('cargo', 'info_add', putout_error_mes)
    get_error_mes('cargo','info')