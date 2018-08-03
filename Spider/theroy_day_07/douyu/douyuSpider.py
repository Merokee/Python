# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-17 下午7:59
import requests
from bs4 import BeautifulSoup
import unittest
from pymongo import MongoClient
from selenium import webdriver


class DouyuSpider(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        self.base_url = "https://www.douyu.com/directory/all"
        self.client = MongoClient()  # 不传表示默认本机
        self.collection = self.client.spider.douyu
        self.count = 1

    def testDouyu(self):
        self.driver.get(self.base_url)
        while True:
            html = self.driver.page_source

            soup = BeautifulSoup(html, "lxml")
            node = soup.select_one("#live-list-content")
            title_list = node.select('h3[class="ellipsis"]')
            tag_list = node.select('span[class="tag ellipsis"]')
            master_list = node.select('span[class="dy-name ellipsis fl"]')
            public_list = node.select('span[class="dy-num fr"]')

            for title, tag, master, public in zip(title_list, tag_list, master_list, public_list):
                item = {}
                item["title"] = title.string.strip()
                item["tag"] = tag.string.strip()
                item["master"] = master.string.strip()
                item["public"] = public.string.strip()

                self.collection.insert(item)
            print("[INFO]正在爬取第{}页".format(self.count))
            self.count += 1
            next = soup.select("#J-pager .shark-pager-disable-next")
            if len(next):
                break

            self.driver.find_element_by_css_selector(
                "#J-pager .shark-pager-next").click()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()