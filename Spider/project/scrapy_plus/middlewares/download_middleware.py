# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午7:57


class DownloadMiddleware(object):
    def process_request(self, request, spider):
        print("[DownloadMid] process_request:<{}>".format(request.url))
        return request

    def process_response(self, response, spider):
        print("[DownloadMid] process_response:<{}>".format(response.url))
        return response