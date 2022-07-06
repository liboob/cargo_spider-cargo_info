# -*- coding: utf-8 -*-


import logging

import pymongo
import json
import pymysql

from scrapy_rabbitmq_scheduler.spiders import RabbitSpider

# from cargo_info.cargo_info.items import CargoInfoItem
# from cargo_info.items import CargoInfoItem
from info.cargo_info.items import CargoInfoItem

from common_utils.env_settings import *
from common_utils.common_methods import LoggerClass

logger = logging.getLogger('pika')
logger.setLevel(logging.ERROR)
elk_log = LoggerClass('python-package', 'cargo')


class InfoSpiderSpider(RabbitSpider):
    name = 'info_spider_all'
    allowed_domains = []
    # start_urls = ['http://crates.io/']
    queue_name = 'cargo_info_queue'
    items_key = 'cargo_dep_queue'
    client = pymongo.MongoClient(MONGO_CLIENT)
    db = client['Cargo']
    # collection = db['Cargo_Queue']
    # collection_dep = db['Cargo_dep']
    collection_info_versions = db['Cargo_info_versions']

    conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
                                  port=MYSQL_QUEUE_PORT,
                                  user=MYSQL_QUEUE_USER,
                                  password=MYSQL_QUEUE_PASSWORD,
                                  db=MYSQL_QUEUE_DB,
                                  charset=MYSQL_QUEUE_CHARSET,
                                  cursorclass=pymysql.cursors.DictCursor)
    handle_httpstatus_list = [404, 403]

    def parse(self, response):
        name = response.url[32:]  # 获取package_name
        print(name)
        json_datas = response.text
        json_data = json.loads(json_datas)
        print(response.status)
        if response.status in self.handle_httpstatus_list:
            if response.status == 404:
                sql = 'update  cargo_spider_queue set is_delete=1 where package_name = "{}"'.format(name)
                with self.conn.cursor() as c:
                    c.execute(sql)
                self.conn.commit()
            log_data = {
                'log_type': '爬取',
                'response_status': response.status,
                'request_url': response.request.url,
                'data_content': {
                    'package_name': name,
                    'package_version': None,
                    'package_type': 'cargo'
                }
            }
            elk_log.error(f'url:{response.url} is {response.status}', extra=log_data)

        if response.status == 200:
            crate = json_data.get('crate')  # 获取info信息
            versions = json_data.get('versions')  # 获取version信息
            crate['versions'] = versions  # 替换info中的version信息
            if crate:
                print(crate)
                res = self.collection_info_versions.update({'id': crate.get('id')}, {'$set': crate}, True, False)
                if res.get('nModified') == 1:
                    self.collection_info_versions.update({'id': crate.get('id')}, {'$unset': {"is_insert": ""}},
                                                         False,True)
                sql = 'update cargo_spider_queue set is_crawl=1 where package_name = "{}"'.format(name)
                with self.conn.cursor() as c:
                    c.execute(sql)
                self.conn.commit()
            version_dep_url = []
            for version in versions:
                dep_url = "https://crates.io/" + version['links']['dependencies']
                version_dep_url.append(dep_url)
            item = CargoInfoItem()
            item['package_name'] = name
            item['dep_version_url'] = version_dep_url
            print(item)
            yield item


if __name__ == '__main__':
    os.system("scrapy crawl info_spider_all")
    # cmdline.execute(['scrapy', 'crawl', 'info_spider'])
