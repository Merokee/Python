"""思路"""
# 分析贴吧URL:# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=50
# pn=(page-1) * 50
# 请求贴吧URL，提取帖子URL
# 请求帖子URL，提取图片URL
# 请求图片URL，获取图片html，保存bytes类型文件

from urllib import request
from urllib import parse
from lxml import etree


class TiebaSpider:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    def send_request(self, tieba_url):
        req = request.Request(tieba_url, headers=self.headers)
        response = request.urlopen(req)
        return response.read()

    def extract_tizi_url(self, tiba_html):
        html_obj = etree.HTML(tiba_html)
        tizi_url_list = html_obj.xpath('//a[@class="j_th_tit "]/@href')
        return ["https://tieba.baidu.com/" + x for x in tizi_url_list]

    def extract_img_url(self, tizi_html):
        html_obj = etree.HTML(tizi_html)
        img_url_list = html_obj.xpath('//img[@class="BDE_Image"]/@src')
        return img_url_list

    def write_file(self, img_url, img_html):
        with open ("李毅吧/" + img_url[-10:], "wb") as f:
            f.write(img_html)

    def start(self, page_num, tieba_name):
        for page in range(1, page_num + 1):
            query_dict = {"kw": tieba_name, "ie": "utf-8", "pn": (page-1) * 50}
            tieba_url = "https://tieba.baidu.com/f?" + parse.urlencode(query_dict)
            tieba_html = self.send_request(tieba_url)
            tizi_url_list = self.extract_tizi_url(tieba_html.decode("utf-8"))
            for tizi_url in tizi_url_list:
                tizi_html = self.send_request(tizi_url)
                img_url_list = self.extract_img_url(tizi_html.decode("utf-8"))
                for img_url in img_url_list:
                    img_html = self.send_request(img_url)
                    self.write_file(img_url, img_html)


if __name__ == '__main__':
    tieba_name = input("输入贴吧名字；")
    page_num = input("页数：")
    spider = TiebaSpider()
    spider.start(page_num,tieba_name)
