from urllib import request
from urllib import parse
from lxml import etree
# input_content = input("输入你想点评的内容：")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
# path_str = parse.quote(input_content)  # 编码字符串
# for x in range(1, 5):
req = request.Request("https://777av.vip/html/tupian/yazhou/2018/0322/412422.html", headers=headers)
response = request.urlopen(req)
html_obj = etree.HTML(response.read().decode("utf-8"))
tieba_img_list = html_obj.xpath('//img/@src')
tieba_img_list.pop(0)
for img in tieba_img_list:
    img = "https:" + img
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    req = request.Request(img, headers=headers)
    response = request.urlopen(req)
    print(img)
    # req = request.Request(img, headers=headers)
    # response_ = request.Request(req)
    # print(response)
    with open("huangtu/" + img[-10:], "wb") as f:
        f.write(response.read())
# print(tieba_img_list)
