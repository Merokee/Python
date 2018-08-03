# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:36
from lxml import etree
import re
import json


class Response(object):
    def __init__(self, url, body, headers=None, status_code=None, encoding=None, request=None):
        self.url = url
        self.body = body
        self.headers = headers
        self.encoding = encoding
        self.request = request

    def xpath(self, rule):
        html_obj = etree.HTML(self.body)
        return html_obj.xpath(rule)

    def find_all(self, rule):
        return re.findall(self.body, rule)

    @property
    def json(self):
        try:
            return json.loads(self.body)
        except Exception as e:
            raise e