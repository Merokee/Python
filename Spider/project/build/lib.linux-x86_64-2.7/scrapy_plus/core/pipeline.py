# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:37


# 框架初期调试使用，成型框架使用的是用户settings配置的管道
class Pipeline(object):
    def process_item(self, item, spider):
        with open("item.str", "a") as f:
            f.write(str(item.data))
