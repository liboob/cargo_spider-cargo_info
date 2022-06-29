import json
import logging
import math
import logstash
import socket
import pymysql
import pika
from common_utils.env_settings import *

class LoggerClass(logging.Logger):
    def __init__(self, springAppName='python-logstash', active='logger', logstash_host=ELK_HOST,
                 logstash_port=ELK_PORT, version=1,
                 logger_name="python-logstash-logger", is_print=1, extra=None,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        '''
        :param springAppName:日志分类 python-spider/python-package/python-project
        :param active:具体名称 npm/php/github-50-star
        :param is_print:是否需要将日志打印
        :param extra:传递的额外参数
        :param fmt:日志打印的格式
        '''
        logging.Logger.__init__(self, name=springAppName + '-' + active)
        self.extra = self._set_extra(active, springAppName, extra)
        self.setLevel(logging.INFO)
        self.addHandler(logstash.TCPLogstashHandler(logstash_host, logstash_port, version=version))
        if is_print:
            self.addHandler(logging.StreamHandler())
            format_str = logging.Formatter(fmt)
            self.handlers[1].setFormatter(format_str)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        if extra:
            extra.update(self.extra)
        else:
            extra = self.extra
        super()._log(level, msg, args, exc_info=None, extra=extra, stack_info=False)

    def _set_extra(self, active, springAppName, extra):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        default_extra = {
            "active": active,
            "springAppName": springAppName,
            "host": host,
            "hostname": hostname
        }
        if extra is None:
            extra = dict()
        extra.update(default_extra)
        return extra


class LjIdClass(object):
    def __init__(self):
        self.mysql_conn = pymysql.connect(host=MYSQL_17_HOST,
                                          port=MYSQL_17_PORT,
                                          user=MYSQL_17_USER,
                                          password=MYSQL_17_PASSWORD,
                                          db=MYSQL_17_DB,
                                          charset=MYSQL_17_CHARSET,
                                          cursorclass=pymysql.cursors.DictCursor)
        self.mysql_queue_conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
                                                port=MYSQL_QUEUE_PORT,
                                                user=MYSQL_QUEUE_USER,
                                                password=MYSQL_QUEUE_PASSWORD,
                                                db=MYSQL_QUEUE_DB,
                                                charset=MYSQL_QUEUE_CHARSET,
                                                cursorclass=pymysql.cursors.DictCursor)

        # self.logger = LoggerClass('python-package', 'lj_id', is_print=1)

    def get_lj_package_id(self, package_name, package_type, table_name):
        with self.mysql_conn.cursor() as cursor:
            sql = "SELECT id,project_id FROM lj_id.lj_id_map_package where package_name = '{}' and type = '{}'".format(
                package_name,package_type)
            print(sql)
            cursor.execute(sql)
            data = cursor.fetchone()
        if not data:
            with self.mysql_queue_conn.cursor() as cursor_queue:
                sql = "insert ignore into package_spider_queue.%s(package_name) values ('%s')" % (
                    table_name, package_name)
                cursor_queue.execute(sql)


                self.mysql_queue_conn.commit()  # 云服务器
            self._map_lj_id_one(package_type, package_name)
            with self.mysql_conn.cursor() as cursor:
                sql = "SELECT id,project_id FROM lj_id.lj_id_map_package where package_name = '{}' and type = '{}'".format(
                    package_name,package_type)
                cursor.execute(sql)
                data = cursor.fetchone()
        if not data:
            lj_id = None
            # self.logger.error("{} 的 {} 包 lj_package_id 生成异常".format(package_type, package_name))
        else:
            # self.logger.info("{} 的 {} 包 lj_package_id 生成成功".format(package_type, package_name))
            lj_id = data['id']
        return lj_id

    def _map_lj_id_one(self, package_type, package_name):
        sql = "insert ignore into lj_id.lj_id_map_package (package_name, type) values ('{}', '{}')".format(package_name,
                                                                                                           package_type)
        with self.mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            self.mysql_conn.commit()

    def map_lj_id_all(self, package_type, table_name):
        insert_sql = "insert ignore into lj_id.lj_id_map_package (package_name, type) values ('{}', '{}')"

        sql = "select package_name from package_spider_queue.%s where map_lj_id = 0" % table_name
        update_sql = "update package_spider_queue.%s set map_lj_id = 1 where package_name = '{}'" % table_name

        if package_type == 'maven':
            sql = "select package_path from package_spider_queue.%s where map_lj_id = 0" % table_name
            update_sql = "update package_spider_queue.%s set map_lj_id = 1 where package_path = '{}'" % table_name

        # TODO 修改rds配置
        with self.mysql_queue_conn.cursor() as cursor_queue:
            cursor_queue.execute(sql)
            result = cursor_queue.fetchall()
            with self.mysql_conn.cursor() as cursor:
                for i in result:
                    try:
                        package_name = i['package_name']
                        insert_sql_result = insert_sql.format(package_name, package_type)
                        cursor.execute(insert_sql_result)
                        update_sql_result = update_sql.format(package_name)
                        cursor_queue.execute(update_sql_result)
                        self.mysql_conn.commit()
                        self.mysql_queue_conn.commit()
                    except:
                        pass


def get_insert_sql(insert_data, table_name):
    datas = insert_data.items()
    insert_data_key = ','.join([x[0] for x in datas])
    data_value = [x[1] for x in datas]
    num_s = ('%s,' * len(insert_data))[:-1]
    update_data_key = ','.join([x[0] + '=%s' for x in datas])
    sql_insert = f'INSERT INTO `{table_name}`({insert_data_key}) VALUES({num_s}) ON DUPLICATE KEY UPDATE {update_data_key};'
    return sql_insert, data_value


def get_sql_select_id(data, table_name):
    query_fields = ["package_name", "lj_package_id", "version", "package_version", "dependency_package_name",
                    "dependency_package_version", "dependency_environment"]
    sql_list = []
    for each in query_fields:
        if each in data.keys():
            if data[each] is None:
                sql_list.append(f'{each} is null')
            else:
                sql_list.append(f'{each} = "{data[each]}"')
    sql_query = ' and '.join(sql_list)
    sql_select_id = f"select id from {table_name} where {sql_query}"
    return sql_select_id


def get_increment_sql(increment_data, table_name, increment_id, is_insert):
    datas = increment_data.items()
    insert_data_key = ','.join([x[0] for x in datas])
    data_value = [x[1] for x in datas]
    num_s = ('%s,' * len(increment_data))[:-1]
    sql_increment = f"insert into {table_name} (id,is_insert,time,{insert_data_key}) VALUES({increment_id},{is_insert},curdate(),{num_s})"
    return sql_increment, data_value


def get_encrypt_sql(data, table_name, increment_id, is_insert, encrypt_fields):
    encrypt_fields = encrypt_fields
    encrypt_data = {}
    for each in encrypt_fields:
        encrypt_data[each] = data[each]
        data.pop(each)

    datas = encrypt_data.items()
    insert_data_key_encrypt = ','.join([x[0] for x in datas])
    data_value_encrypt = [x[1] for x in datas]
    num_s_encrypt = ("HEX(AES_ENCRYPT(%s,'LJQC_FOSSEYE_2020_888888'))," * len(encrypt_data))[:-1]

    other_data = data
    datas = other_data.items()
    insert_data_key_other = ','.join([x[0] for x in datas])
    data_value_other = [x[1] for x in datas]
    num_s_other = ('%s,' * len(other_data))[:-1]

    data_value = data_value_encrypt + data_value_other

    sql_increment = f"insert into {table_name} (id,is_insert,time,{insert_data_key_encrypt},{insert_data_key_other}) VALUES({increment_id},{is_insert},curdate(),{num_s_encrypt},{num_s_other})"
    print(sql_increment % tuple(data_value))
    return sql_increment, data_value


def data_to_cnnvd(insert_data, conn, table_name, increment_fields, encrypt_fields):
    increment_table_name = table_name + '_increment'
    increment_data = {}
    for each in increment_fields:
        increment_data[each] = insert_data[each]
    sql_insert, data_value = get_insert_sql(insert_data, table_name)
    with conn.cursor() as cursor:
        is_insert = cursor.execute(sql_insert, data_value * 2)  # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
        if is_insert != 0:
            sql_select_id = get_sql_select_id(insert_data, table_name)
            cursor.execute(sql_select_id)
            increment_id = cursor.fetchone()[0]
            sql_increment, data_value = get_encrypt_sql(increment_data, increment_table_name, increment_id, is_insert, encrypt_fields)
            cursor.execute(sql_increment, data_value)
    conn.commit()


def data_to_db(insert_data, conn, table_name, increment_fields):
    '''
    :param table_info: 表的连接、数据库、表名信息
    :param insert_data: 插入的数据，字典形式-->{'字段名':值}
    :param incre_table_info: 增量表的连接、数据库、表名信息
    :param increment_fields: ["lj_package_id", "package_name", "home_page", "first_release_time", "latest_release_time",
                    "latest_release", "description", "language", "keywords", "license", "verified_license"]
                    ["package_name","lj_package_id","version","published_time","license","verified_license"]
                    ["lj_package_id","package_version","dependency_package_name","dependency_package_version"]
    :return:
    '''
    increment_table_name = table_name + '_increment'
    increment_data = {}
    for each in increment_fields:
        increment_data[each] = insert_data[each]
    sql_insert, data_value = get_insert_sql(insert_data, table_name)
    with conn.cursor() as cursor:
        is_insert = cursor.execute(sql_insert, data_value * 2)  # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
        if is_insert != 0:
            sql_select_id = get_sql_select_id(insert_data, table_name)
            cursor.execute(sql_select_id)
            increment_id = cursor.fetchone()[0]
            sql_increment, data_value = get_increment_sql(increment_data, increment_table_name, increment_id, is_insert)
            cursor.execute(sql_increment, data_value)
    conn.commit()
    return is_insert

"""
写入文件格式push消息
"""
def publish_file(package_type, msg_type, data_type):
    """
    :param package_type: 包类型 exp:nuget
    :param msg_type: 队列类型 exp: info,version
    :param data_type: 数据类型 exp: str,list
    :return:
    """
    with open('./homepage_file.txt', 'r', encoding='utf-8') as fp:
        content = fp.readline()
        info_datas = content.split(',,')
        info_datas.remove('')
    publish_message(package_type, msg_type, data_type, info_datas)


"""
mysql查询未爬取包传入info队列
"""
def publish_mysql(package_type, msg_type, host, db):
    """
    :param package_type: 包类型
    :param msg_type: 队列类型
    :param host: 数据库地址
    :param db: 库名
    :return:
    """
    conn = pymysql.connect(host=host,
                           user='root',
                           port=3306,
                           password='ti9#aN%^^ToqacQD',
                           db=db,
                           charset='utf8')
    cursor = conn.cursor()
    sql = f'SELECT homepage FROM `{package_type}_spider_queue` WHERE is_crawl=0'
    cursor.execute(sql)
    datas = cursor.fetchall()
    if datas:
        info_datas = []
        for data in datas:
            homepage = data[0]
            info_datas.append(homepage)
        publish_message(package_type, msg_type, 'list',info_datas)


"""
version消费者启动scrapy并返回ack消息
"""
def consuming_spider(channel, method, header_props, message):
    msg = str(message, encoding='utf-8')
    msg_t = json.loads(msg)
    version_queue = msg_t['version_queue']
    package_name = msg_t['package_name']
    s = len(version_queue)
    if s > 300:
        times = math.ceil(s / 300)
        for t in range(times):
            version_str = ','.join(version_queue[t * 300:(t + 1) * 300])
            os.system(('scrapy crawl version -a version_queue=%s -a package_name=%s' % (version_str, package_name)))
    else:
        version_str = ','.join(version_queue)
        os.system(('scrapy crawl version -a version_queue=%s -a package_name=%s' % (version_str, package_name)))
    publish_message('nuget', 'mysql', 'str', package_name)
    channel.basic_ack(delivery_tag=method.delivery_tag)


"""
启动version爬虫监听脚本或入库监听脚本
"""
def consuming_message(package_type, msg_type, spider_name):
    """
    :param package_type: 包类型
    :param msg_type: 队列类型
    :param spider_name: version_spider消费者函数名
    :return:
    """
    # 定义 AMQP URL，这里使用前文中已经创建好的超级管理员 mickey 和虚拟主机 web_app
    params = pika.URLParameters(f'{RABBITMQ_CONNECTION_PARAMETERS}/{package_type}_vhost?heartbeat=0')

    # 创建与 RabbitMQ 的连接，也称为消息代理连接
    conn = pika.BlockingConnection(params)

    # 新建一个连接中的通道
    channel = conn.channel()

    # 声明一个直连交换机，通过消息路由键和绑定路由键的匹配来完成路由转发策略
    # 参数 durable=True, auto_delete=False 表示希望持久化交换机
    # 其中 durable=True 表示 RabbitMQ 重启后会自动重建该交换机
    channel.exchange_declare(exchange=f'{package_type}_exchange',
                             exchange_type='direct',
                             passive=False,
                             durable=True,
                             auto_delete=False)

    # 声明一个队列，如果生产者将消息发送给了一个不存在的队列，那么 RabbitMQ 会自动丢弃该消息
    channel.queue_declare(queue=f'{package_type}_{msg_type}_queue', arguments={'x-max-priority': 255}, durable = True)

    # 将队列绑定到交换机，并设置一个路由键
    channel.queue_bind(queue=f'{package_type}_{msg_type}_queue',
                       exchange=f'{package_type}_exchange',
                       routing_key=f'{package_type}_{msg_type}_route')

    # 同时处理消息为1条,处理之后再次发送消息
    channel.basic_qos(prefetch_count=1)

    # 指定消费者订阅的队列，并且告诉消息代理需要等待 ACK
    channel.basic_consume(f'{package_type}_{msg_type}_queue',spider_name,False)

    # 开始监听订阅队列，直到 CTRL+C 退出。
    try:
          print(" [*] Waiting for messages. To exit press CTRL+C")
          channel.start_consuming()
    except KeyboardInterrupt as err:
          channel.stop_consuming()

    conn.close()


"""
rabbitmq生产者
"""
# 发送消息
def publish_message(package_type, msg_type, data_type, info_datas):
    """
    :param package_type: 包类型
    :param msg_type: 队列类型
    :param data_type: 数据类型 exp: str,list
    :param info_datas: 传入的数据列表
    :return:
    """
    # 同样需要建立连接和通道
    params = pika.URLParameters(f'{RABBITMQ_CONNECTION_PARAMETERS}/{package_type}_vhost?heartbeat=0')
    conn = pika.BlockingConnection(params)
    channel = conn.channel()
    # 将在生产者中声明的 RabbitMQ 对象再重新声明一次，如果已经存在了则不会重复创建
    # 这段逻辑实际上可有可无，只是为了说明声明一个 RabbitMQ 对象并不表示一定会创建
    # 只有在第一次声明该对象的时候才会创建，之后无论在生成者或消费者中都可以再次声明
    channel.exchange_declare(exchange=f'{package_type}_exchange',
                             exchange_type='direct',
                             passive=False,
                             durable=True,
                             auto_delete=False)
    channel.queue_declare(queue=f'{package_type}_{msg_type}_queue', arguments={'x-max-priority': 255}, durable = True)
    channel.queue_bind(queue=f'{package_type}_{msg_type}_queue', exchange=f'{package_type}_exchange',
                       routing_key=f'{package_type}_{msg_type}_route')
    # 同时处理消息为1条,处理之后再次发送消息
    channel.basic_qos(prefetch_count=1)
    # 配置 AMQP 消息的 BasicProperties 基本属性
    # 在 AMQP 协议中定义了 14 种 Properties，会随消息一同传递，这里表示使用 JSON 格式数据流
    # 参数 delivery_mode=2 表示希望持久化消息，在 RabbitMQ 重启后自动重建消息
    # props = pika.BasicProperties(content_type='application/json', delivery_mode=2)
    props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
    if data_type == 'list':
        for info_data in info_datas:
            body = info_data
            # body = json.dumps(info_data)
            # 发布消息，指定消息传递的交换机和所携带的路由键
            channel.basic_publish(exchange=f'{package_type}_exchange',
                                  routing_key=f'{package_type}_{msg_type}_route',
                                  body=body,
                                  properties=props)
            print(" [x] Publish {}".format(info_data))
    elif data_type == 'str':
        body = info_datas
        # body = json.dumps(info_data)
        # 发布消息，指定消息传递的交换机和所携带的路由键
        channel.basic_publish(exchange=f'{package_type}_exchange',
                              routing_key=f'{package_type}_{msg_type}_route',
                              body=body,
                              properties=props)
        print(" [x] Publish {}".format(info_datas))
    conn.close()
