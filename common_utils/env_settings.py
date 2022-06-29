# -*- coding: utf-8 -*-
import os

IP = '39.107.36.205'
# IP = '172.17.39.200'

ELK_HOST = os.getenv('ELK_HOST', '182.150.57.8')
ELK_PORT = os.getenv('ELK_PORT', 5044)

# lj_id生成数据库
# MYSQL_17_HOST = os.getenv('MYSQL_17_HOST', 'rm-2zed9e3s0xa04m7q39o.mysql.rds.aliyuncs.com')
# MYSQL_17_PORT = int(os.getenv('MYSQL_17_PORT', 3306))
# MYSQL_17_USER = os.getenv('MYSQL_17_USER', 'fosseye')
# MYSQL_17_PASSWORD = os.getenv('MYSQL_17_PASSWORD', 'Abc$1234')
# MYSQL_17_DB = os.getenv('MYSQL_17_DB', 'lj_id')
# MYSQL_17_CHARSET = os.getenv('MYSQL_17_CHARSET', 'utf8')
MYSQL_17_HOST = os.getenv('MYSQL_17_HOST', '127.0.0.1')
MYSQL_17_PORT = int(os.getenv('MYSQL_17_PORT', 3306))
MYSQL_17_USER = os.getenv('MYSQL_17_USER', 'root')
MYSQL_17_PASSWORD = os.getenv('MYSQL_17_PASSWORD', '123456')
MYSQL_17_DB = os.getenv('MYSQL_17_DB', 'lj_id')
MYSQL_17_CHARSET = os.getenv('MYSQL_17_CHARSET', 'utf8')

# mysql数据存储数据库
# MYSQL_HOST = os.getenv('MYSQL_HOST', 'rm-2zed9e3s0xa04m7q39o.mysql.rds.aliyuncs.com')
# MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
# MYSQL_USER = os.getenv('MYSQL_USER', 'fosseye')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Abc$1234')
# MYSQL_DB = os.getenv('MYSQL_DB', 'fosseye')
# MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')
MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
MYSQL_DB = os.getenv('MYSQL_DB', 'fosseye')
MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')

# # mysql队列表数据库
# MYSQL_QUEUE_HOST = os.getenv('MYSQL_QUEUE_HOST', '172.17.39.200')
# MYSQL_QUEUE_PORT = int(os.getenv('MYSQL_QUEUE_PORT', 50001))
# MYSQL_QUEUE_USER = os.getenv('MYSQL_QUEUE_USER', 'root')
# MYSQL_QUEUE_PASSWORD = os.getenv('MYSQL_QUEUE_PASSWORD', 'prismguard@123')
# MYSQL_QUEUE_DB = os.getenv('MYSQL_QUEUE_DB', 'package_spider_queue')
# MYSQL_QUEUE_CHARSET = os.getenv('MYSQL_QUEUE_CHARSET', 'utf8mb4')
MYSQL_QUEUE_HOST = os.getenv('MYSQL_QUEUE_HOST', '127.0.0.1')
MYSQL_QUEUE_PORT = int(os.getenv('MYSQL_QUEUE_PORT', 3306))
MYSQL_QUEUE_USER = os.getenv('MYSQL_QUEUE_USER', 'root')
MYSQL_QUEUE_PASSWORD = os.getenv('MYSQL_QUEUE_PASSWORD', '123456')
MYSQL_QUEUE_DB = os.getenv('MYSQL_QUEUE_DB', 'package_spider_queue')
MYSQL_QUEUE_CHARSET = os.getenv('MYSQL_QUEUE_CHARSET', 'utf8mb4')

# redis链接
REDIS_HOST = os.getenv('REDIS_HOST', '172.17.39.200')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'L&d!e3.$*1om2&')

# mongo数据库
# MONGO_HOST = os.getenv('MONGO_HOST', '172.17.39.200')
MONGO_HOST = os.getenv('MONGO_HOST', '39.107.36.205')
MONGO_PORT = int(os.getenv('MONGO_PORT', 50002))
MONGO_USER = os.getenv('MONGO_USER', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'pFFOdfJR8*I3WteU')
MONGO_CLIENT = os.getenv('MONGO_CLIENT', f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}')

# Rabbitmq链接
# RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '172.17.39.200')
# RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
# RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'mickey')
# RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'qwer123wasd')
# RABBITMQ_CONNECTION_PARAMETERS = \
#     os.getenv('RABBITMQ_CONNECTION_PARAMETERS',
#               f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_CONNECTION_PARAMETERS = \
    os.getenv('RABBITMQ_CONNECTION_PARAMETERS',
              f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}')

# 代理池链接
# PROXY_HOST = '172.17.39.200'
PROXY_HOST = '39.107.36.205'
PROXY_PORT = 5002
PROXY_URL = os.getenv('PROXY_URL', f'http://{PROXY_HOST}:{PROXY_PORT}/random')

# 数据清洗链接
# DATA_PROCESS_HOST = os.getenv('DATA_PROCESS_HOST', '172.17.39.200')
DATA_PROCESS_HOST = os.getenv('DATA_PROCESS_HOST', '39.107.36.205')
DATA_PROCESS_PORT = os.getenv('DATA_PROCESS_PORT', 8080)
LICENSE_URL = os.getenv('LICENSE_URL', f'http://{DATA_PROCESS_HOST}:{DATA_PROCESS_PORT}/license/extract')
