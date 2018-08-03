# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:37
import chardet

import requests
from ..http.response import Response


class Downloader(object):
    def send_request(self, request):
        if request.method.upper() == "GET":
            response = requests.get(
                url=request.url,
                headers=request.headers,
                proxies=request.proxy,
                data=request.params
            )
        elif request.method.upper() == "POST":
            response = requests.post(
                url=request.url,
                headers=request.headers,
                proxies=request.proxy,
                data=request.formdata
            )
        else:
            raise Exception("Don't Support request method: <{}>".format(request.method))

        return Response(
            url=response.url,
            body=response.content,
            headers=response.headers,
            encoding=chardet.detect(response.content)["encoding"],
            request=request
        )
