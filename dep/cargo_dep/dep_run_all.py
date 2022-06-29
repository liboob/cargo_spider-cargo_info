import json
import math
import os
import time
import threading

import pymysql
import common_utils.common_methods as CM
from common_utils.env_settings import *

logger = CM.LoggerClass('python-package', 'cargo', is_print=1)


package_type = 'cargo'
# conn = pymysql.connect(host=MYSQL_QUEUE_HOST, port=MYSQL_QUEUE_PORT, user=MYSQL_QUEUE_USER,
#                        password=MYSQL_QUEUE_PASSWORD, database=MYSQL_QUEUE_DB, charset=MYSQL_QUEUE_CHARSET)

# def publish_info_queue():
#     while 1:
#         with conn.cursor(pymysql.cursors.DictCursor) as c:
#             for i in range(1000):
#                 sql = 'SELECT * FROM `cargo_spider_queue` where is_crawl = 0 and is_delete = 0 limit {},500'.format(
#                     i * 500)
#                 c.execute(sql)
#                 url_data = []
#                 for result in c.fetchall():
#                     if result is None:
#                         sql = 'update  cargo_spider_queue set is_crawl=0 where is_crawl=1'
#                         with conn.cursor() as cursor:
#                             cursor.execute(sql)
#                         conn.commit()
#                         conn.cursor()
#                         break
#                     name = result.get('package_name')
#                     url = 'https://crates.io/api/v1/crates/{}'.format(name)
#                     url_data.append(url)
#                 CM.publish_message(package_type, 'info', 'list', url_data)  # 入口队列产生



def dep_monitor(package_type):
    print('开始监控dep队列')
    CM.consuming_message(package_type, 'dep', dep_main)


# def mysql_monitor(package_type):
#     print('开始监控入库队列')
#     CM.consuming_message(package_type, 'mysql', mysql_main)


def dep_main(channel, method, header_props, message):
    msg = str(message, encoding='utf-8')
    msg_t = json.loads(msg)
    dep_version = msg_t['dep_version_url']
    package_name = msg_t['package_name']
    s = len(dep_version)
    if s > 200:
        times = math.ceil(s / 200)
        for t in range(times):
            dep_url_str = ','.join(dep_version[t * 200:(t + 1) * 200])
            os.system(('scrapy crawl cargo_dep_all -a dep_url_str=%s -a package_name=%s' % (dep_url_str, package_name)))
    else:
        dep_url_str = ','.join(dep_version)
        os.system(('scrapy crawl cargo_dep_all -a dep_url_str=%s -a package_name=%s' % (dep_url_str, package_name)))
    CM.publish_message(package_type, 'mysql', 'str', package_name)
    channel.basic_ack(delivery_tag=method.delivery_tag)
#
#
# def mysql_main(channel, method, header_props, message):
#     msg = str(message, encoding='utf-8')
#     msg_t = json.loads(msg)
#     package_name = msg_t['package_name']
#     print(package_name)
#     INFO.info_main(package_name)
#     DEP.dep_main(package_name)
#     channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    while 1:
        # dep_monitor(package_type)
        # print("sleep 1111111111111111")
        if threading.activeCount() < 6:
            t = threading.Thread(target=dep_monitor, args=(package_type,))
            t.start()
        time.sleep(1)
