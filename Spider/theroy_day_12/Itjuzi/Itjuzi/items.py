# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    company_slogan = scrapy.Field()
    company_info = scrapy.Field()
    company_url = scrapy.Field()
    company_intro = scrapy.Field()
    main_page = scrapy.Field()
    financing_list = scrapy.Field()
    ext_financing_set = scrapy.Field()
    product = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_spider = scrapy.Field()

