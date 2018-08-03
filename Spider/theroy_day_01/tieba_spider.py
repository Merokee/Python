#!/usr/lib/env python
#-*- coding:utf8 -*-

import urllib2, random, urllib, sys


# 贴吧爬虫

def tieba_spider(tieba_name, total_page):
    url_perfix = 'http://tieba.baidu.com/f?'
    useragent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like     Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML,     like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like     Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko)     Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like     Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Geck    o) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko)     Chrome/19.0.1084.36 Safari/536.5",
    ]
    
    query_list = []
    for page in range(total_page):
        query_dict = {'wd':tieba_name, 'pn':page*50}
        query_list.append(urllib.urlencode(query_dict))

    url_list = [url_perfix + q for q in query_list]

    for index, url in enumerate(url_list):
        request = urllib2.Request(url, headers = {'User-Agent':random.choice(useragent_list)})
        response = urllib2.urlopen(request)
        html = response.read()

        with open('tieba_html/'+ tieba_name + '吧' + 'page=' + str(index + 1), 'wb') as f:
            f.write(html)
            print(tieba_name + '吧' + 'page=' + str(index + 1) + '爬取成功')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('运行方式：\r\npython2 tieba_spider.py 贴吧名 总页数')

    tieba_name = sys.argv[1]
    total_page = int(sys.argv[2])
    tieba_spider(tieba_name, total_page)
