# 定义请求头，拼接URL
# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=50
# 获取响应html文件
# 用xpath提取目标子节点URL
# 获取图片html文件
# 写入李毅吧文件夹
from urllib import request
from lxml import etree
from urllib import parse
import time


class TiebaSpider:
    def __init__(self):
        # 使用IE的代理，因为目标服务器会对发送到其它浏览器代理的内容进行优化，可能会注释js代码，这样我们爬去的链接就无法执行了
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    def send_request(self, url):
        req = request.Request(url, headers=self.headers)
        response = request.urlopen(req)
        return  response.read()  # 返回bytes类型网页代码

    def splice_url(self, tieba_name, page):
        query_dict = {"kw": tieba_name, "ie": "utf-8", "pn": (page-1)*50}
        url = parse.urlencode(query_dict)
        return "https://tieba.baidu.com/f?" + url

    def extract_ziba_url(self, tieba_html):
        html_obj = etree.HTML(tieba_html)
        ziba_url_list = html_obj.xpath('//a[@class="j_th_tit "]/@href')
        return ["https://tieba.baidu.com/"+x for x in ziba_url_list]

    def extract_img_url(self, img_html):
        html_obj = etree.HTML(img_html)
        img_url_list = html_obj.xpath('//img[@class="BDE_Image"]/@src')
        return img_url_list

    def writ_file(self, img_url, img_html):
        with open("李毅吧/"+img_url[-10:], "wb") as f:
            print("【Info】:%s保存成功！" % img_url[-10:])
            f.write(img_html)

    def start(self, tieba_name, page_num):
        for page in range(1, page_num+1):
            tieba_url = self.splice_url(tieba_name, page)
            print(tieba_url)
            tieba_html = self.send_request(tieba_url).decode("utf-8")
            ziba_url_list = self.extract_ziba_url(tieba_html)
            for ziba_url in ziba_url_list:
                print(ziba_url)
                ziba_html = self.send_request(ziba_url).decode("utf-8")
                img_url_list = self.extract_img_url(ziba_html)
                for img_url in img_url_list:
                    print(img_url)
                    img_html = self.send_request(img_url)
                    self.writ_file(img_url, img_html)
                    time.sleep(1)



if __name__ == '__main__':
    tieba_name = input("贴吧名：")
    page_num = int(input("页数："))
    spider= TiebaSpider()
    spider.start(tieba_name, page_num)

