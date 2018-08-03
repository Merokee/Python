# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-12 下午3:45
import requests
# import json

from bs4 import BeautifulSoup
from pymongo import *


class PositionSpider(object):
    def __init__(self):
        self.base_url = "https://hr.tencent.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        self.page = 1
        # self.position_list = []

    def __open(self):
        self.client = MongoClient(host="localhost", port=27017)
        self.collection = self.client["spider"]["tencent"]

    def send_request(self, url):
        response = requests.get(url, headers=self.headers)
        print("[INFO]正在爬取第{}页的所有职位信息{}".format(self.page,url))
        return response.content

    def parse_page(self, html):
        soup = BeautifulSoup(html, "lxml")
        node_list = soup.select(".even, .odd")
        for node in node_list:
            item = {}
            item["detail_url"] = self.base_url + node.a.get('href')
            detail_html = self.send_request(item["detail_url"])
            detail_item = self.parse_detail(detail_html)
            item["position_name"] = node.a.get_text()
            item["position_type"] = node.select("td")[1].string
            item["people_count"] = node.select("td")[2].string
            item["address"] = node.select("td")[3].string
            item["create_time"] = node.select("td")[4].string
            item.update(detail_item)
            self.collection.insert(item)
        if not soup.find("a", {"id": "next", "class": "noactive"}):
            return self.base_url + soup.find("a", {"id": "next"}).get("href")
        return False

    def parse_detail(self, html):
        soup = BeautifulSoup(html, "lxml")
        ul_list = soup.select(".squareli")
        item = {}
        item["work_duty"] = [i.string for i in ul_list[0].select("li")]
        item["work_require"] = [i.string for i in ul_list[1].select("li")]
        return item

    # def save_file(self):
    #     json.dump(self.position_list, open("position.json", "w"))

    def main(self):
        self.__open()
        start_url = "https://hr.tencent.com/position.php?&start=0"
        html = self.send_request(start_url)
        while self.page < 5:
            url = self.parse_page(html)
            if not url:
                break
            html = self.send_request(url)
            self.page += 1
        # self.save_file()


if __name__ == '__main__':
    spider = PositionSpider()
    spider.main()
