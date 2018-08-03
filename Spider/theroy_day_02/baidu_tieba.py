#!/usr/lib/env python
# -*- coding:utf8 -*-

import urllib, urllib2


class Tieba_Spider:
    """
    爬去百度贴吧某吧指定页
    """

    def __init__(self):
        self.url_prefix = 'http://tieba.baidu.com/f?'
        self.headers = {
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        }
        self.tieba_name = str(raw_input('请输入贴吧名：'))
        self.start_page = int(raw_input('起始页名：'))
        self.end_page = int(raw_input('结束页名：'))

    def send_request(self, url):
        """
        发送请求
        :param url: 请求地址
        :return: bytes文件
        """
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()

    def save_html(self, filename, content):
        """
        保存html
        :param filename: 文件名
        :param content: 内容
        :return: None
        """
        with open(filename, 'w') as f:
            f.write(content)

    def start(self):
        """
        任务调度器
        :return: None
        """
        for n, page in enumerate(range(self.start_page, self.end_page + 1)):
            pn = (page - 1) * 50
            query_dict = {'kw': self.tieba_name, 'pn': pn}
            query_str = urllib.urlencode(query_dict)
            url = self.url_prefix + query_str
            content = self.send_request(url)
            filename = str(n + self.start_page) + '.html'
            self.save_html(filename, content)
            print(filename)


if __name__ == '__main__':
    spider = Tieba_Spider()
    spider.start()
