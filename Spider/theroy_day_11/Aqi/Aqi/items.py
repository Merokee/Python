# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    aqi = scrapy.Field()
    quality_grade = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm10 = scrapy.Field()
    so2 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3_8h = scrapy.Field()
    crawl_spider = scrapy.Field()
    crawl_time = scrapy.Field()
