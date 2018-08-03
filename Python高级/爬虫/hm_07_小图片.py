from urllib import request
# from urllib import parse
from lxml import etree
# https://tieba.baidu.com/f?ie=utf-8&kw=动物


class TeibaSpider:
    # 贴吧爬虫
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    def send_request(self, url):
        # 请求响应 返回bytes类型代码
        req = request.Request(url, headers=self.headers)
        response = request.urlopen(req)
        return response.read()

    def extract_tiezi_url(self, html):
        # 用xpath解析获得新的url
        html_obj = etree.HTML(html)
        tieba_url_list = html_obj.xpath('//a/@href')
        # 返回url
        return ["https://777av.vip" + x for x in tieba_url_list]

    def extract_img_url(self, html):
        html_obj = etree.HTML(html)
        tieba_img_list = html_obj.xpath('//img/@src')
        return tieba_img_list

    def write_file(self, file_content, file_name):
        with open("哈士奇图片/"+file_name, "wb") as f:
            f.write(file_content)
            print("【info】:正在保存%s" % file_name)

    def start(self):
        # for page in range(1, page_num+1):
            # 写请求头
            # query_dict = {"ie": "utf-8", "kw": teiba_name, "pn": (page - 1) * 50}
        url = "https://777av.vip"
        # # 获取贴吧响应代码
        html = self.send_request(url)
        # # 解析代码获取子吧url列表
        tieba_url_list = self.extract_tiezi_url(html.decode("utf-8"))
        for tieba_url in tieba_url_list:
            img_html =self.send_request(tieba_url)
            img_list =self.extract_img_url(img_html.decode("utf-8"))
            # 获取图片bytes 并保存
            for img in img_list:
                img_ = self.send_request(img)
                self.write_file(img_, img[-10:])
            # print("第%d页爬取成功" % page)


if __name__ == '__main__':
    # teiba_name = input("贴吧名：")
    # page_num = int(input("想爬的页数："))
    spider = TeibaSpider()
    spider.start()


