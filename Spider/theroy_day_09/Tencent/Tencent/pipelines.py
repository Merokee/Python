# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .items import TencentDetailItem, TencentListItem


class TencentListPipeline(object):
    """将所有信息保存在一个文件中"""
    def open_spider(self, spider):
        self.f = open("tencent_list.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        if isinstance(item, TencentListItem):
            data = json.dumps(dict(item))
            self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()


class TencentDetailPipeline(object):
    """将所有信息保存在一个文件中"""
    def open_spider(self, spider):
        self.f = open("tencent_detail.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        if isinstance(item, TencentDetailItem):
            data = json.dumps(dict(item))
            self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()
