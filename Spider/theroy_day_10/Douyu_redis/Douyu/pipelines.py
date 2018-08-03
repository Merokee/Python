# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
import scrapy
import os

from .settings import IMAGES_STORE
from scrapy.pipelines.images import ImagesPipeline


class DouyuImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['vertical_src'])

    def item_completed(self, results, item, info):

        old_path = IMAGES_STORE + [x["path"] for ok, x in results if ok][0]
        new_path = IMAGES_STORE + "images/" + item["nick_name"] + ".jpg"
        try:
            os.rename(old_path, new_path)
        except:
            pass
        item["image_path"] = new_path
        return item


class DouyuPipeline(object):
    def open_spider(self, spider):
        self.f = open("douyu.json", "w")
        self.f.write("[\n")

    def process_item(self, item, spider):
        item["time"] = str(datetime.now())
        data = json.dumps(dict(item))
        self.f.write(data + ",\n")
        return item

    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()
