# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-26 下午4:37
from datetime import datetime
import importlib
import time

# from spider import Spider
from scheduler import Scheduler
from downloader import Downloader
# from pipeline import Pipeline

# from ..middlewares.download_middleware import DownloadMiddleware
# from ..middlewares.spider_middleware import SpiderMiddleware

from ..http.request import Request
from ..items import Item

from ..untils.logger import logger
from ..conf.default_settings import *

if ASYNC_TYPE == "coroutine":
    from ..async.coroutine import Pool
    logger.info("ASYNC TYPE ：<{}>".format(ASYNC_TYPE))
elif ASYNC_TYPE == "thread":
    from multiprocessing.dummy import Pool
    logger.info("ASYNC TYPE ：<{}>".format(ASYNC_TYPE))
else:
    logger.info("Don't support ASYNC TYPE ：<{}>".format(ASYNC_TYPE))


class Engine(object):
    def __init__(self):
        self.spiders = self._auto_import_moudle_cls(SPIDERS, is_spider=True)
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = self._auto_import_moudle_cls(PIPELINES)
        self.spider_mids = self._auto_import_moudle_cls(SPIDER_MIDDLEWARES)
        self.download_mids = self._auto_import_moudle_cls(DOWNLOADER_MIDDLEWARES)
        self.pool = Pool(ASYNC_COUNT)
        self.total_response = 0
        self.is_running = True

    def _auto_import_moudle_cls(self, path_list, is_spider=False):
        if not is_spider:
            instances = []
        else:
            instances = {}

        for path in path_list:
            module_name = path[:path.rfind(".")]
            class_name = path[path.rfind(".") + 1:]
            result = importlib.import_module(module_name)
            cls = getattr(result, class_name)

            if not is_spider:
                instances.append(cls())
            else:
                instances[cls.name] = cls()
        return instances

    def start(self):
        # 开始时间
        start = datetime.now()
        logger.info("Start time : {}".format(start))

        self._start_engine()

        # 结束时间
        end = datetime.now()
        logger.info("End time : {}".format(end))

        # 总计运行时间
        logger.info("Useing time : {}".format((end - start).total_seconds()))

    def _callback(self, _):
        """在请求发送出去等待响应时，继续发送请求"""

        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        """主逻辑函数"""
        if ROLE is None or ROLE == "master":
            # 异步构造请求
            self.pool.apply_async(self._execute_start_requests())

        elif ROLE is None or ROLE == "slave":
            # 异步发送请求, 获取响应，处理响应
            for _ in range(ASYNC_COUNT):
                self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

        # 等待请求完全响应
        while True:
            time.sleep(0.01)
            if self.total_response == self.scheduler.total_request and self.total_response !=0:
                self.is_running = False
                break

        # 原生协程池没有close方法，我们可以自定义类继承协程池类，新建一个close方法，实现代码的兼容
        self.pool.close()
        self.pool.join()
        logger.info("Main Thread is over!")

    def _execute_start_requests(self):
        for spider_name, spider in self.spiders.items():
            request_list = spider.start_requests()
            # 给每个请求添加爬虫名属性
            for request in request_list:
                request.spider_name = spider_name

                # 经过所有爬虫中间件的处理后给调度器去重
                for spider_mid in self.spider_mids:
                    request = spider_mid.process_request(request, spider)

                logger.info("Request_url: <{}>".format(request.url))
                self.scheduler.add_request(request)

    def _execute_request_response_item(self):

        # 从调度器获取请求
        request = self.scheduler.get_request()
        # 没有请求直接结束程序
        if not request:
            return

        # 获取当前请求对应的爬虫对象
        spider = self.spiders[request.spider_name]
        for download_mid in self.download_mids:
            # 下载中间件处理请求
            request = download_mid.process_request(request, spider)
        # 下载器发送请求
        response = self.downloader.send_request(request)
        logger.info("Response_url: <{}>".format(response.url))
        for download_mid in self.download_mids:
            # 下载中间件处理响应
            response = download_mid.process_response(response, spider)

        callback_func = getattr(spider, request.callback)
        # 解析响应
        parse_result = callback_func(response)

        # 响应计数
        self.total_response += 1
        print(self.total_response, "*"*40)

        for item_or_request in parse_result:
            # 返回请求对象，则重新构建请求，获取响应
            if isinstance(item_or_request, Request):
                for spider_mid in self.spider_mids:
                    request = spider_mid.process_request(item_or_request, spider)
                self.scheduler.add_request(request)

            # 返回item对象, 交给中间件处理, 交由管道处理
            elif isinstance(item_or_request, Item):
                for spider_mid in self.spider_mids:
                    item = spider_mid.process_item(item_or_request, spider)
                # 爬虫中间件处理完之后交给管道处理
                for pipeline in self.pipelines:
                    pipeline.process_item(item, spider)

            # 非可处理对象，抛出异常
            else:
                raise Exception("Don't support data type: <{}>".format(type(item_or_request)))
