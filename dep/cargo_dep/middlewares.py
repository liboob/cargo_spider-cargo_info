from scrapy import signals
import requests
from twisted.internet.error import TimeoutError


class ProxychiMiddleware(object):
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    # 定义一个请求之前的方法
    def process_request(self, request, spider):
        # 随机获取一个代理
        proxy = requests.get(self.proxy_url).text
        request.meta['proxy'] = 'https://' + proxy
        # ua = faker.Faker(locale='zh_CN').chrome()
        # request.headers.setdefault('User-Agent', ua)
        return None

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception, TimeoutError):
            return request

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('PROXY_URL'))
