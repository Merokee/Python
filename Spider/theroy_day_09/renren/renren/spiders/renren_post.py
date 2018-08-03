# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-21 下午5:48
import scrapy


class RenRen(scrapy.Spider):
    name = "renren_post"

    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"

        yield scrapy.FormRequest(
            url=url,
            formdata={
                "email": "mr_mao_hacker@163.com",
                "password": "alarmchime"
            },
            callback=self.parse
        )

    def parse(self, response):
        urls = {
            "http://www.renren.com/327550029/profile",
            "http://www.renren.com/410043129/profile"
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        file_name = response.xpath("//title/text()").extract_first()

        with open(file_name, "w") as f:
            f.write(response.body)
