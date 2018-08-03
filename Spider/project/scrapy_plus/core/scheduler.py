# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:37

# 针对Python2,Python3导入Queue
# try:
#     from queue import Queue
# except:
#     from Queue import Queue
import six
# from six.moves.queue import Queue
# 调用兼容的Queue类(将redis的rpush,lpop集成为put,get方法)
from ..untils.logger import logger
from ..queue.queue import Queue

from ..conf.default_settings import *

if ROLE is None:
    from ..queue.set import NormalFilterSet as Set

    logger.info("ROLE is <{}>".format(ROLE))
elif ROLE in ['master', 'slave']:
    from ..queue.set import RedisFilterSet as Set

    logger.info("ROLE is <{}>".format(ROLE))
else:
    raise ImportError("Not EXIST ROLE: <{}>".format(ROLE))


class Scheduler(object):
    """
    调度器，对请求放入任务队列并进行去重，并返回请求url
    """

    def __init__(self):
        self._filter_set = Set()
        self.queue = Queue()
        self.total_request = 0

    def add_request(self, request):
        if request.dont_filter:
            self.queue.put(request)
            self.total_request += 1
        else:
            if self._filter_request(request):
                self.queue.put(request)
                # 规整url,并生成指纹
                fp = self._get_fingerprint(request)
                self._filter_set.add_fp(fp)
                self.total_request += 1

    def get_request(self):
        try:
            return self.queue.get(False)
        except Exception:
            return False

    def _filter_request(self, request):
        fp = self._get_fingerprint(request)
        if not self._filter_set.is_filter(fp):
            return True
        else:
            logger.info("Filter request: [{}] <{}>".format(request.method, request.url))
            return False

    def _get_fingerprint(self, request):
        import w3lib.url
        from hashlib import sha1

        # 对url地址进行规整排序处理
        url = w3lib.url.canonicalize_url(request.url)

        # 将请求方法转为大写处理
        method = request.method.upper()

        # 保证返回一个字典（不管用户有没有传参，面sha1生成数据出错）
        params = request.params if request.params else {}
        params = str(sorted(params.items(), key=lambda x: x[0]))

        formdata = request.formdata if request.formdata else {}
        formdata = str(sorted(formdata.items(), key=lambda x: x[0]))

        sha1_data = sha1()
        # update()必须接收一个字节码字符串  python2 str unicode, python3 bytes str
        sha1_data.update(self._get_utf8_str(url))
        sha1_data.update(self._get_utf8_str(method))
        sha1_data.update(self._get_utf8_str(params))
        sha1_data.update(self._get_utf8_str(formdata))

        # 生成一个16进制数的字符串，做为请求指纹
        fp = sha1_data.hexdigest()

        return fp

    # 判断字符串的类型，如果是Unicode则转为utf-8
    def _get_utf8_str(self, string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:
                return string.encode("utf-8")
        else:
            if isinstance(string, bytes):
                return string
            else:
                return string.encode("utf-8")
