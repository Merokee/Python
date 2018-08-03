# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-29 下午4:40
# 导入两个爬虫类，用来判断item数据所属spider，并分别处理
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class BaiduPipeline1(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("[BaiduPipeline1]: item data : {}".format(type(item.data)))

        return item


class BaiduPipeline2(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("[BaiduPipeline2]: item data : {}".format(type(item.data)))

        return item


class DoubanPipeline1(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print("[DoubanPipeline1]: item data : {}".format(type(item.data)))

        return item


class DoubanPipeline2(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print("[DoubanPipeline2]: item data : {}".format(type(item.data)))

        return item