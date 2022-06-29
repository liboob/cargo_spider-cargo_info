import os
import time

while 1:
    os.system("python Cargo_Queue_Spider.py")
    os.system("scrapy crawl info_spider_all")
    print("start sleeping~~~~~~~")
    time.sleep(86400)
