# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CargoInfoItem(scrapy.Item):
    package_name = scrapy.Field()
    dep_version_url = scrapy.Field()
