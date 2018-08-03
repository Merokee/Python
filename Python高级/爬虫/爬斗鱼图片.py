# 请求到斗鱼分类网页的内容
# 提取出所有的图片地址
# 利用协程来爬图片

from urllib import request
from lxml import etree
import multiprocessing


def getImg():
    req = request.Request("https://www.douyu.com/directory", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"})
    response = request.urlopen(req)
    douyuHtml = response.read().decode("utf-8")
    objHtml = etree.HTML(douyuHtml)
    imgUrlList = objHtml.xpath('//img[@class="preview"]/@data-original')
    print(imgUrlList)
    for imgUrl in imgUrlList:
        print(imgUrl, "*"*20)
        response = request.urlopen(imgUrl)
        imgHtml = response.read()
        with open("douyu/" + imgUrl[-10:], "wb") as f:
            f.write(imgHtml)
        print("保存图片完成")


q = multiprocessing.Manager().Queue()
po = multiprocessing.Pool(10)
for _ in range(10):
    po.apply_async(getImg)

po.close()
po.join()