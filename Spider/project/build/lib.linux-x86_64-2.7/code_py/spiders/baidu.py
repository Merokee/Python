# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-29 下午3:18
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.items import Item


class BaiduSpider(Spider):
    name = "baidu"
    start_urls = ["http://www.baidu.com/",
                  "http://news.baidu.com"]

    def start_requests(self):
        for url in self.start_urls:
            # 不指定callback，默认响应由parse解析
            yield Request(url)

    def parse(self, response):
        item = {}
        item['title'] = response.xpath("//head/title/text()")[0]
        yield Item(item)

