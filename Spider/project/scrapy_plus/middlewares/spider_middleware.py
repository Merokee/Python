# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午7:57


class SpiderMiddleware(object):
    def process_request(self, request):
        print("[SpiderMid] process_request:<{}>".format(request.url))
        return request

    def process_item(self, item):
        print("[SpiderMid] process_item:<{}>".format(str(item.data)))
        return item
