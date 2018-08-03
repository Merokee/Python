# coding:utf-8

import scrapy

from ItcastSpider.items import ItcastspiderItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml"]

    def parse(self, response):
        node_list = response.xpath("//div[@class='li_txt']")

        for node in node_list:
            item = ItcastspiderItem()

            item["name"] = node.xpath("./h3/text()").extract_first()
            item["grade"] = node.xpath("./h4/text()").extract_first()
            item["info"] = node.xpath("./p/text()").extract_first()

            yield item
