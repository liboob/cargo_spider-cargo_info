import requests
import pymongo
import time
import pymysql
from env_setting import *

client = pymongo.MongoClient(MONGO_CLIENT)
db = client['Cargo']
collection = db['Cargo_Queue']

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


def xx(x):
    # 爬取队列
    for page in range(x, 2):
        # try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        print('当前爬取第{}页'.format(page))
        url = 'https://crates.io/api/v1/crates?page={}&per_page=50&sort=alpha'.format(page)
        response = requests.get(url=url, headers=headers, timeout=15, verify=False)
        print(response.status_code)
        json_datas = response.json()  # 字典
        crates = json_datas.get('crates')
        page += 1
        if crates:
            with conn.cursor() as c:
                for result in crates:
                    package_name = result.get('id')
                    sql = 'INSERT ignore INTO cargo_spider_queue(package_name) VALUES ("{}")'.format(package_name)
                    c.execute(sql)
                    conn.commit()
            time.sleep(3)
        else:
            print('结束')
            break
        # except:
        #     xx(page)


# while 1:
xx(1)
