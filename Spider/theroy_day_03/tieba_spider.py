# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-11 下午4:25
import requests
from lxml import etree
import os


class TiebaSpider(object):
    """
        爬取百度贴吧的图片
    """
    def __init__(self):
        self.base_url = "http://tieba.baidu.com"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.tieba_name = raw_input("想爬取的贴吧名：")
        self.start_page = int(raw_input("想爬去的起始页：").decode('utf-8'))
        self.end_page = int(raw_input("想爬去的结束页：").decode('utf-8'))

    def send_request(self, url, query_dict=None):
        """
        发送请求
        :param url: 请求地址
        :param query_dict: 查询字符串
        :return: bytes类型html
        """
        try:
            response = requests.get(url, params=query_dict, headers=self.headers)
            return response.content
        except Exception as e:
            print e, "请求<{}>失败".format(url)


    def parse_page(self, html):
        """
        使用xpath获取href属性值
        :param html: html文档
        :return: href属性
        """
        selector = etree.HTML(html)
        page_url_list = selector.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/@href')
        return page_url_list

    def parse_image(self, html):
        """
        获取image的src属性
        :param html: html
        :return: 图片地址
        """
        selector = etree.HTML(html)
        image_url_list = selector.xpath('//img[@class="BDE_Image"]/@src')
        return image_url_list

    def save_file(self, filename, image):
        """
        创立单独的文件夹，保存文件
        :param filename: 文件名
        :param image: bytes类型图片html
        :return: ok
        """
        with open(filename, 'wb') as f:
            print("[INFO] 下载图片成功　<{}>".format(filename))
            f.write(image)

    def main(self):
        """
        调度器
        :return: ok
        """
        directory_name = self.tieba_name + "吧图片"
        try:
            os.mkdir(directory_name)
        except:
            pass
        # 切换到文件夹
        os.chdir(directory_name)

        # 获取详情地址列表
        for page in range(self.start_page, self.end_page + 1):
            pn = (page-1)*50
            query_dict = {"kw": self.tieba_name, "pn":pn}
            url = self.base_url + "/f?"
            page_html = self.send_request(url, query_dict)
            page_url_list = self.parse_page(page_html)

            # 获取图片地址列表
            for detail_url in page_url_list:
                url = self.base_url + detail_url
                detail_html = self.send_request(url)
                image_url_list = self.parse_image(detail_html)

                # 下载图片
                for image_url in image_url_list:
                    image = self.send_request(image_url)
                    filename = image_url[-10:]
                    self.save_file(filename, image)


if __name__ == "__main__":
    spider = TiebaSpider()
    spider.main()
