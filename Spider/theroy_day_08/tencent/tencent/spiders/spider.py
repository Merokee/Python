# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentJsonItem, TencentDetailItem


class SpiderSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["hr.tencent.com"]
    base_url = 'http://hr.tencent.com/position.php?&start='
    # start_urls中是一批次的请求url,构建url列表实现高并发
    start_urls = [base_url + str(page) for page in range(0, 3691, 10)]

    def parse(self, response):

        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentJsonItem()
            item["position_address"] = u"http://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item["position_name"] = node.xpath("./td[1]/a/text()").extract_first()
            item["position_type"] = node.xpath("./td[2]/text()").extract_first()
            item["people_count"] = node.xpath("./td[3]/text()").extract_first()
            item["work_place"] = node.xpath("./td[4]/text()").extract_first()
            item["create_time"] = node.xpath("./td[5]/text()").extract_first()

            yield item

            request = scrapy.Request(item["position_address"], meta={"item":item}, callback=self.parse_detail)
            yield request

    # 用于处理详情页
    def parse_detail(self, response):
        # 保存到不同的item中
        # item = TencentDetailItem()

        # 保存在一条信息中，使用meta传递参数
        item = response.meta["item"]

        node_list = response.xpath("//ul[@class='squareli']")
        item["work_duty"] = ";".join(node_list[0].xpath("li").extract())
        item["work_require"] = ";".join(node_list[1].xpath("li").extract())
        return item
