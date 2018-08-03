# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:36


class Item(object):
    """
    框架提供的Item类，保存解析后的数据，使用item.data获取
    """
    def __init__(self, data):
        # 定义私有属性，只允许访问不允许修改
        self._data = data

    @property
    def data(self):
        return self._data