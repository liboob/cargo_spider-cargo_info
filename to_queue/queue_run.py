import time

import pymysql

import common_utils.common_methods as CM
from common_utils.env_settings import *

"""
从mysql队列取出 放入rabbitmq队列
"""

package_type = 'cargo'
conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
                       port=MYSQL_QUEUE_PORT,
                       user=MYSQL_QUEUE_USER,
                       password=MYSQL_QUEUE_PASSWORD,
                       db=MYSQL_QUEUE_DB,
                       charset=MYSQL_QUEUE_CHARSET,
                       cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    i = 0
    with conn.cursor(pymysql.cursors.DictCursor) as c:
        while 1:
            # if i == 0:
            #     os.system("python Cargo_Queue_Spider.py")
            #     pass
            sql = 'SELECT * FROM `cargo_spider_queue` where is_crawl = 0 and is_delete = 0 limit {},500'.format(
                i * 500)

            c.execute(sql)
            url_data = []
            for result in c.fetchall():
                name = result.get('package_name')
                url = 'https://crates.io/api/v1/crates/{}'.format(name)
                url_data.append(url)
            if len(url_data) == 0:
                sql = 'update  cargo_spider_queue set is_crawl=0 where is_crawl=1'
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                conn.commit()
                print('start sleeping')
                i = 0
                time.sleep(86400 * 7)

                continue
            CM.publish_message(package_type, 'info', 'list', url_data)  # 入口队列产生
            i = i + 1
            print(i)
