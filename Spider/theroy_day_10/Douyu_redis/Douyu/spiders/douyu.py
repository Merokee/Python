# -*- coding: utf-8 -*-
import scrapy
import json

from ..items import DouyuItem
from scrapy_redis.spiders import RedisSpider


class DouyuSpider(RedisSpider):
    name = "douyu"
    redis_key = "myspider:start_urls"
    # allowed_domains = ["douyucdn.cn"]
    base_url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    offset = 0
    # start_urls = [base_url + str(offset)]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))

        # 修改这里的类名为当前类名
        super(DouyuSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = json.loads(response.body)["data"]
        if data_list is None:
            return

        for data in data_list:
            item = DouyuItem()
            item["room_link"] = "https://www.douyu.com/" + data["room_id"]
            item["vertical_src"] = data["vertical_src"]
            item["anchor_city"] = data["anchor_city"]
            item["room_name"] = data["room_name"]
            item["nick_name"] = data["nickname"]
            yield item

        self.offset += 20
        yield scrapy.Request(url=self.base_url + str(self.offset), callback=self.parse)



