# Scrapy settings for cargo_info project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from common_utils.env_settings import *

BOT_NAME = 'cargo_info'

SPIDER_MODULES = ['cargo_info.spiders']
NEWSPIDER_MODULE = 'cargo_info.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'cargo_info (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'cargo_info.middlewares.CargoInfoSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'cargo_info.middlewares.CargoInfoDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'cargo_info.pipelines.CargoInfoPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
DEFAULT_REQUEST_HEADERS = {
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': 'https://crates.io/crates/abi_stable',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 50
DOWNLOAD_TIMEOUT = 15
CONCURRENT_REQUESTS_PER_DOMAIN = 50
CONCURRENT_REQUESTS_PER_IP = 50
COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = False
# DOWNLOAD_DELAY = 1/6
RETRY_ENABLED = False
"""
Rabbitmq Settings
"""
# 指定项目的调度器
SCHEDULER = 'scrapy_rabbitmq_scheduler.scheduler.SaaS'

# 指定rabbitmq的连接DSN
RABBITMQ_CONNECTION_PARAMETERS = RABBITMQ_CONNECTION_PARAMETERS + "/cargo_vhost"

# 指定重试的http状态码(重新加回队列重试)
SCHEDULER_REQUEUE_ON_STATUS = []
# SCHEDULER_REQUEUE_ON_STATUS = []

# 指定下载器中间件, 确认任务是否成功
DOWNLOADER_MIDDLEWARES = {
    'scrapy_rabbitmq_scheduler.middleware.RabbitMQMiddleware': 999,
    'cargo_info.middlewares.ProxychiMiddleware': 90,
}
# 指定item处理方式, item会加入到rabbitmq中, 不需要把item写入到rabbitmq的话, 别加这个
ITEM_PIPELINES = {
    'scrapy_rabbitmq_scheduler.pipelines.RabbitmqPipeline': 300,
}
RABBITMQ_DURABLE = True  # 是否持久化队列, True为持久化 False为非持久化, 默认True
RABBITMQ_CONFIRM_DELIVERY = True  # 消息是否需要确认, True为需要, False为不需要, 默认是True

PROXY_URL = PROXY_URL
