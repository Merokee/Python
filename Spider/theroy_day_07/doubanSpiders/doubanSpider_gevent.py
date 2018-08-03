# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-17 下午3:20
import time
import gevent
from gevent import monkey
from Queue import Queue

import requests
from lxml import etree

monkey.patch_all()


class DoubanSpider(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.base_url = "https://movie.douban.com/top250?start="
        self.data_queue = Queue()

    def send_request(self, url):
        print("[INFO:] 正在请求", url)
        html = requests.get(url, headers=self.headers).content
        self.parse_page(html)
        return

    def parse_page(self, html):
        selector = etree.HTML(html)
        node_list = selector.xpath('//div[@class="info"]')
        for node in node_list:
            title = node.xpath('.//span[@class="title"]/text()')[0]
            score = node.xpath('.//span[@class="rating_num"]/text()')[0]
            intro_list = node.xpath('.//span[@class="inq"]/text()')
            intro = intro_list[0] if intro_list else ""
            print(title + "\t\t" + score + "\t\t" + intro)

    def main(self):
        url_list = [self.base_url + str(page) for page in range(0, 226, 25)]

        # task_list = []
        # for url in url_list:
        #     spawn = gevent.spawn(self.send_request, url)
        #     task_list.append(spawn)
        #
        # gevent.joinall(task_list)

        gevent.joinall([gevent.spawn(self.send_request,url) for url in url_list])


if __name__ == '__main__':
    start = time.time()
    spider = DoubanSpider()
    spider.main()
    interval = time.time() - start
    print("耗时：{}".format(interval))