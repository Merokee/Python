# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-30 上午10:00
from gevent.pool import Pool as Coroutine_Pool
import gevent.monkey
gevent.monkey.patch_all()


class Pool(Coroutine_Pool):

    def apply_async(self, func, args=None, kwds=None, callback=None):
        return Coroutine_Pool().apply_async(func, args=args, kwds=kwds, callback=callback)

        # python2中super()只支持继承object的类
        # return super(self).apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        pass