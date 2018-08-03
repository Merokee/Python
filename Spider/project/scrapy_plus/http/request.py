# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:36


class Request(object):
    """
    构建请求
    """
    def __init__(self, url, method="GET", headers=None, proxy=None, formdata=None, params=None, callback="parse", dont_filter=False):
        self.url = url
        self.method = method
        self.headers = headers
        self.proxy = proxy
        self.formdata = formdata
        self.params = params
        self.callback=callback
        self.dont_filter = dont_filter



