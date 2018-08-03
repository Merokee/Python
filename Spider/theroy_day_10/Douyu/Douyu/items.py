# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    room_link = scrapy.Field()
    vertical_src = scrapy.Field()
    anchor_city = scrapy.Field()
    nick_name = scrapy.Field()
    room_name = scrapy.Field()
    # 保存在本地的地址
    image_path = scrapy.Field()
    # 下载时间
    time = scrapy.Field()
