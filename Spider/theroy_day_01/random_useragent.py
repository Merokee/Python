#!/usr/lib/env python
#-*- coding:utf8 -*-

import urllib2
import random
import time

def spider():

    # url列表
    url_list=[
        'http://www.httpbin.org/headers',
        'http://www.httpbin.org/headers',
        'http://www.httpbin.org/headers'
    ]

    # User-Agent列表
    useragent_list=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
          
    ]
    
    # 循环url_list并随机user_agent
    for url in url_list:
        request = urllib2.Request(url, headers={'User-Agent':random.choice(useragent_list)})
        response = urllib2.urlopen(request)
        print(response.read())
        time.sleep(2)

if __name__ == '__main__':
    spider()

