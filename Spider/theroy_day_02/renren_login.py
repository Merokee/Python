# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-11 下午4:11
import urllib2, urllib, cookielib


def renren_login():
    # post请求数据
    post_url = "http://www.renren.com/PLogin.do"
    form_dict = {"email": "mr_mao_hacker@163.com", "password": "alarmchime"}
    form_data = urllib.urlencode(form_dict)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(handler)
    request = urllib2.Request(post_url, form_data, headers=headers)
    opener.open(request)

    url_list = [
        "http://www.renren.com/410043129/profile",
        "http://www.renren.com/410043129/profile"
    ]

    for n, url in enumerate(url_list):
        request = urllib2.Request(url, headers=headers)
        response = opener.open(request)
        content = response.read()
        with open('renren_' + str(n) + '.html', 'w') as f:
            f.write(content)


renren_login()