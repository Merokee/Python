# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-21 下午4:24
# import random
# import logging
#
# from .settings import PROXY_LIST
# from .settings import USER_AGENT_LIST
#
#
# class RandomUserAgentMiddleware(object):
#     def process_request(self, request, spider):
#         user_agent = random.choice(USER_AGENT_LIST)
#         request.headers["User-Agent"] = user_agent
#         logging.info(request.headers)
#
#
# class RandomProxyMiddleware(object):
#     def process_request(self, request, spider):
#         proxy = random.choice(PROXY_LIST)
#         request.meta["proxy"] = proxy


from .settings import USER_AGENT_LIST
#from settings import PROXY_LIST
import random
import logging


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = user_agent
        logging.info(request.headers)


class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        #request.meta['proxy'] ="http://115.28.141.184:16816"
        request.meta['proxy'] ="http://maozhaojun:ntkn0npx@115.28.141.184:16816"


