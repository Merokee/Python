# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-11 下午7:47
import re
from random_agent_proxy import generate_agent_proxy
import requests


class DuanziSpider(object):
    def __init__(self):
        self.url = "https://www.neihan8.com/article/list_5_"
        self.page = 1
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.find_page = re.compile(r'<div class="f18 mb20">(.*?)</div>', re.S)
        self.pattern_content = re.compile(r'(&.*?;)|(<.*?>)|\s|　')

    def send_request(self, url):
        response = requests.get(url, headers=self.headers, proxies=generate_agent_proxy()[1])
        return response.content

    def parse_html(self, html):
        utf8_html = html.decode("gbk").encode("utf-8")
        content = self.find_page.findall(utf8_html)
        return content

    def save_file(self, content_list):
        with open('duanzi.txt', "a") as f:
            f.write("第" + str(self.page) + "页\n")
            for content in content_list:
                result = self.pattern_content.sub("", content)
                f.write(result)
                f.write('\n')
            f.write('\n\n')

    def main(self):
        while True:
            if raw_input("Enter表示爬取下一页类容,q表示退出:") == "q":
                return
            url = self.url + str(self.page) + ".html"
            html = self.send_request(url)
            content_list = self.parse_html(html)
            self.save_file(content_list)
            self.page += 1

if __name__ == '__main__':
    spider = DuanziSpider()
    spider.main()