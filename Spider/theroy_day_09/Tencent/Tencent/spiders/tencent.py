# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from Tencent.items import TencentListItem, TencentDetailItem


class TencentSpider(CrawlSpider):
    name = "tencent"
    allowed_domains = ["hr.tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php?start=0&#a"
    ]
    rules = [
        Rule(link_extractor=LinkExtractor(r"start=\d+"), callback="parse_page", follow=True),
        Rule(link_extractor=LinkExtractor(r"position_detail.php\?id=\d+"), callback="parse_detail", follow=False),
    ]

    def parse_page(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentListItem()
            item["position_address"] = u"http://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item["position_name"] = node.xpath("./td[1]/a/text()").extract_first()
            item["position_type"] = node.xpath("./td[2]/text()").extract_first()
            item["people_count"] = node.xpath("./td[3]/text()").extract_first()
            item["work_place"] = node.xpath("./td[4]/text()").extract_first()
            item["create_time"] = node.xpath("./td[5]/text()").extract_first()

            yield item

    # 用于处理详情页
    def parse_detail(self, response):
        item = TencentDetailItem()

        node_list = response.xpath("//ul[@class='squareli']")
        item["work_duty"] = ";".join(node_list[0].xpath("li").extract())
        item["work_require"] = ";".join(node_list[1].xpath("li").extract())
        yield item