import requests
import pymongo
import time
import pymysql
from common_utils.env_settings import *

# 爬取所有包名入mysql队列


client = pymongo.MongoClient(MONGO_CLIENT)
db = client['Cargo']
collection = db['Cargo_Queue']
#
conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
                       port=MYSQL_QUEUE_PORT,
                       user=MYSQL_QUEUE_USER,
                       password=MYSQL_QUEUE_PASSWORD,
                       db=MYSQL_QUEUE_DB,
                       charset=MYSQL_QUEUE_CHARSET,
                       cursorclass=pymysql.cursors.DictCursor)


def proxy():
    proxy = requests.get(PROXY_URL).text
    proxies = {
        # 'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    return proxies


def xx(url):
    # try:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }
    payload = {'api_key': 'a9dd9f7af76ecd5c56d7f4c3b06ab9b9', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)
    # response = requests.get(url=url, headers=headers, timeout=15, proxies=proxy(), verify=False)
    print(response.status_code)
    json_datas = response.json()  # 字典
    crates = json_datas.get('crates')
    if crates:
        with conn.cursor() as c:
            for item in crates:
                package_name = item.get('id')
                sql = 'INSERT ignore INTO cargo_spider_queue(package_name) VALUES ("{}")'.format(package_name)
                c.execute(sql)
                print(sql)
                conn.commit()
    # meta = json_datas.get("meta")
    # next_page = meta.get('next_page')
    # if next_page:
    #     next_url = 'https://crates.io/api/v1/crates' + next_page
    #     print(next_url)
    #     xx(next_url)
    # else:
    #     print('结束')



for _ in range(850):
    url = f'https://crates.io/api/v1/crates?page={_}&per_page=100&sort=alpha'
    try:
        xx(url)
    except Exception as e:
        print(e)
        continue