# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:36

from ..http.request import Request
# from ..items import Item


class Spider(object):
    start_urls = []

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise Exception("Must overwrite function: parse")
        # content = {"content": response.body}
        # item = Item(content)
        # return item

