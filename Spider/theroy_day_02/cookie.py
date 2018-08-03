# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-11 下午3:43
import urllib2
import cookielib

# 构建一个CookieJar对象实例来保存cookie
cookiejar = cookielib.CookieJar()

# 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
handler=urllib2.HTTPCookieProcessor(cookiejar)

# 通过 build_opener() 来构建opener
opener = urllib2.build_opener(handler)

# 4. 以get方法访问页面，访问之后会自动保存cookie到cookiejar中
opener.open("https://www.baidu.com/")

## 可以按标准格式将保存的Cookie打印出来
cookieStr = ""
for item in cookiejar:
    cookieStr = cookieStr + item.name + "=" + item.value + ";"

## 舍去最后一位的分号
print cookieStr[:-1]
