# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentListItem(scrapy.Item):
    position_address = scrapy.Field()
    position_name = scrapy.Field()
    position_type = scrapy.Field()
    people_count = scrapy.Field()
    work_place = scrapy.Field()
    create_time = scrapy.Field()


class TencentDetailItem(scrapy.Item):
    work_duty = scrapy.Field()
    work_require = scrapy.Field()
