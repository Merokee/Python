# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-19 下午4:29
import scrapy
from baidu.items import BaiduItem


class BaiduSpider(scrapy.Spider):
    # 爬虫名，在执行　scrapy crawl 爬虫名　时使用
    name = "baidu"
    # 允许访问的域名，如果给引擎的url域名不在该列表中，则不会交由下载器执行
    allowed_domians = ["baidu.com"]
    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        item = BaiduItem()

        item["title"] = response.xpath("//title/text()").extract_first()

        print(item)
        return item
