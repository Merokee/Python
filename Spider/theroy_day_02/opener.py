# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午9:42
import urllib2

# 构建一个HTTPHandler 处理器对象，支持处理HTTP请求，同时开启Debug Log，debuglevel 值默认 0
http_handler = urllib2.HTTPHandler(debuglevel=1)
# https_handler = urllib2.HTTPSHandler(debuglevel=1)

# 使用urllib2.build_opener创建opener对象
opener = urllib2.build_opener(http_handler)

request = urllib2.Request('http://www.baidu.com')
response = opener.open(request)
print(response.read())

