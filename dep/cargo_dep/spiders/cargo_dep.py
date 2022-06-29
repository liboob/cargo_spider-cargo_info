# -*- coding: utf-8 -*-
import scrapy
import pymongo
import json
import pymysql
import os
from common_utils.env_settings import *

class DepSpider(scrapy.Spider):
    name = 'cargo_dep'
    allowed_domains = []
    client = pymongo.MongoClient(MONGO_CLIENT)
    db = client['Cargo']
    collection = db['Cargo_Queue']
    collection_dep = db['Cargo_dep']
    collection_info_versions = db['Cargo_info_versions']

    conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                           password=MYSQL_PASSWORD, database=MYSQL_DB, charset=MYSQL_CHARSET)
    handle_httpstatus_list = [404, 403]

    def __init__(self, dep_url_str, package_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = dep_url_str
        self.package_name = package_name

    def start_requests(self):
        urls = self.start_urls.split(',')
        for url in urls:
            yield scrapy.Request(url=url, method='GET', callback=self.parse)

    def parse(self, response):
        print(response.url)
        name = self.package_name
        version = response.url.split('/')[8]
        json_datas = json.loads(response.text)
        json_datas.update({'id': name, 'verson': version})
        print(json_datas)
        self.collection_dep.update({'id': name, 'verson': version}, {'$set': json_datas}, True, False)
        sql = 'update  cargo_package_versions set is_crawl=1 where package_name = "{}" and version = "{}"'.format(name,
                                                                                                                  version)
        with self.conn.cursor() as c:
            c.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    os.system("scrapy crawl cargo_dep")
