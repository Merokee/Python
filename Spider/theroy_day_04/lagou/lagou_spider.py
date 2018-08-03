# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-12 下午5:11
"""
仿照ajax请求获取职位详情
反爬：请求频率，请求来源，cookie, User-Agent,X-Requested-With
"""
import random
import json
import time

import requests
from jsonpath import jsonpath
from pymongo import *


class LogouSpider(object):
    def __init__(self):
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.headers = {
            "Referer" : "https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&xl=%E6%9C%AC%E7%A7%91&city=%E6%B7%B1%E5%9C%B3&district=%E5%8D%97%E5%B1%B1%E5%8C%BA",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "WEBTJ-ID=20180712171054-1648dc1f2b966-09dad554b0ac4b-6114147a-1049088-1648dc1f2baf6; _ga=GA1.2.742989988.1531386656; user_trace_token=20180712171059-7e4d3f45-85b3-11e8-95db-525400f775ce; LGSID=20180712171059-7e4d43f3-85b3-11e8-95db-525400f775ce; LGUID=20180712171059-7e4d45ce-85b3-11e8-95db-525400f775ce; JSESSIONID=ABAAABAAADEAAFI94269C3B575A8629EA18C67B8A34A949; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531386656,1531386660,1531386673; index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=59f8977409d2409396d0f304351e6c30; TG-TRACK-CODE=search_code; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531388769; LGRID=20180712174612-699bc5a3-85b8-11e8-95e1-525400f775ce",
            "X-Requested-With" : "XMLHttpRequest"
        }
        self.kword = raw_input("查询关键字：")
        self.proxies_list = [
            {'http': 'http://111.231.204.43:7890'},
            {'http': 'http://45.40.194.111:7890'},
            {'http': 'http://139.199.160.42:7890'},
            {"http": "maozhaojun:ntkn0npx@115.28.141.184:16816"},
            {'http': 'http:kaaokou:kaaokou123@47.106.196.9:22222'}
        ]
        # self.item_list = []
        self.page = 1
        self.city = raw_input("要查询的城市：")

    def __open(self):
        self.client = MongoClient("localhost",27017)
        self.collection = self.client["spider"]["lagou"]

    def send_request(self):
        """
        发送请求，query_data表示筛选条件，form_data对应查询关键字和页数
        :return: json对应的python_obj
        """
        query_data = {
            "xl": "本科",
            "px": "default",
            "city": self.city,
            # "district": "福田区",
            "needAddtionalResult": "false"
        }
        form_data = {
            "first": "true",
            "pn": self.page,
            "kd": self.kword
        }
        url = self.base_url + self.kword
        python_obj = requests.post(url, params=query_data, data=form_data, headers=self.headers,
                                 proxies=random.choice(self.proxies_list)).json()
        print("【INFO】正在爬取第{}页".format(self.page))
        return python_obj

    def parse_page(self, python_obj):
        """
        保存详细信息
        :param python_obj: json数据格式的python_obj
        :return: 包含详细信息的json数据
        """
        position_list = jsonpath(python_obj, "$..result")[0]
        for position in position_list:
            item = {}
            item["companyId"] = position["companyId"]
            item["companyShortName"] = position["companyShortName"]
            item["createTime"] = position["createTime"]
            item["positionAdvantage"] = position["positionAdvantage"]
            item["salary"] = position["salary"]
            item["education"] = position["education"]
            item["city"] = position["city"]
            item["positionName"] = position["positionName"]
            item["industryField"] = position["industryField"]
            item["jobNature"] = position["jobNature"]
            item["companySize"] = position["companySize"]
            companylabel_str = ""
            for companylabel in position["companyLabelList"]:
                companylabel_str += companylabel + ", "
            item["companyLabelList"] = companylabel_str
            item["district"] = position["district"]
            item["firstType"] = position["firstType"]
            item["secondType"] = position["secondType"]
            item["companyFullName"] = position["companyFullName"]
            # self.item_list.append(item)
            self.collection.insert(item)

    # def save_file(self):
    #     json.dump(self.item_list, open("lagou.json", "w"))

    def main(self):
        """
        调度器
        :return: 爬取进度
        """
        self.__open()
        while self.page < 20:
            python_obj = self.send_request()
            self.parse_page(python_obj)
            # self.save_file()
            self.page += 1
            time.sleep(random.randint(1,3))


if __name__ == '__main__':
    spider = LogouSpider()
    spider.main()
