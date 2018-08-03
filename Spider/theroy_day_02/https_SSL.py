# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午9:10
import ssl, urllib2

context = ssl._create_unverified_context()

url = 'https://www.12306.cn/mormhweb/'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request, context=context)

print(response.read())
