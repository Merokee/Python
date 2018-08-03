# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import TencentJsonItem, TencentDetailItem


class TencentPipeline(object):
    """将所有信息保存在一个文件中"""
    def open_spider(self, spider):
        self.f = open("tencent_all.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        data = json.dumps(dict(item))
        self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()


class TencentJsonPipeline(object):
    """用于存储列表页的职位信息"""
    def open_spider(self, spider):
        self.f = open("tencent.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        if isinstance(item,TencentJsonItem):
            data = json.dumps(dict(item))
            self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()


class TencentDetailPipeline(object):
    """用于存储详情页职位信息"""
    def open_spider(self, spider):
        self.f = open("tencent.detail", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        if isinstance(item, TencentDetailItem):
            data = json.dumps(dict(item))
            self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()