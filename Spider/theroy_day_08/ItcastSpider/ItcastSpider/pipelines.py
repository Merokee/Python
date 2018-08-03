# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ItcastspiderPipeline(object):
    def open_spider(self, spider):
        self.f = open("itcast.json", "w")
        self.f.write("{\n")

    def process_item(self, item, spider):
        data = json.dumps(dict(item))
        self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("}")
        self.f.close()