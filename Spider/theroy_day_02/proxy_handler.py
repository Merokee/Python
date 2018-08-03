# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午9:49
import urllib2, random

proxy_list = [
    {'http':'111.231.204.43:7890'},
    {'http':'45.40.194.111:7890'},
    {'http':'139.199.160.42:7890'},
]
# 创建处理器
proxy_handler = urllib2.ProxyHandler(random.choice(proxy_list))
# proxy_handler = urllib2.ProxyHandler({})

# 创建opener
opener = urllib2.build_opener(proxy_handler)

request = urllib2.Request('http://httpbin.org/ip')

response = opener.open(request)

print(response.read())

