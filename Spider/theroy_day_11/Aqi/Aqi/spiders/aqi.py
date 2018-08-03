# -*- coding: utf-8 -*-
import scrapy
import urllib

from ..items import AqiItem


class AqiSpider(scrapy.Spider):
    name = "aqi"
    allowed_domains = ["aqistudy.cn"]
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        # 拿到所有子城市的链接　monthdata.php?city=阿坝州
        city_url_list = response.xpath('//div[@class="all"]//ul[@class="unstyled"]//a/@href')
        for city_url in [self.base_url + city_url for city_url in city_url_list]:
            yield scrapy.Request(url=city_url, callback=self.parse_month)

    def parse_month(self, response):
        month_url_list = response.xpath('//tbody//a/@href')
        for month_url in [self.base_url + month_url for month_url in month_url_list]:
            yield scrapy.Request(url=month_url, callback=self.parse_day)

    def parse_day(self, response):
        tr_list = response.xpath('//tbody/tr')[1:]
        # city_name = response.meta['city']
        urlencde_city = response.url[response.url.find("=") + 1: response.url.find("&")]
        # unquote()返回utf-8字符串，再decode() 返回Unicode
        city_name = urllib.unquote(urlencde_city).decode("utf-8")
        for tr in tr_list:
            item = AqiItem()
            item['city'] = city_name
            item['date'] = tr.xpath("./td[1]/text()").extract_first()
            item['aqi'] = tr.xpath("./td[2]/text()").extract_first()
            item['level'] = tr.xpath("./td[3]//text()").extract_first()
            item['pm2_5'] = tr.xpath("./td[4]/text()").extract_first()
            item['pm10'] = tr.xpath("./td[5]/text()").extract_first()
            item['so2'] = tr.xpath("./td[6]/text()").extract_first()
            item['co'] = tr.xpath("./td[7]/text()").extract_first()
            item['no2'] = tr.xpath("./td[8]/text()").extract_first()
            item['o3'] = tr.xpath("./td[9]/text()").extract_first()

            yield item

