# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午4:24

import urllib, urllib2, json
import chardet


class DoubanRank:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "bid=sU8xi1ovUVA; ll=118282; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1531124807%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=Ux40RJQbpuOpPdpimecmpNHSa4jq28kM; _vwo_uuid_v2=DCF4CE6308D6E9807E3E48C7057FE8C8A|fda248e18618f4533aa474ca72ca8036; _pk_id.100001.4cf6=93a1be9b3aa75822.1531124807.1.1531125508.1531124807.",
            "Host": "movie.douban.com",
            "Referer": "https://movie.douban.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        self.url_prefix = "http://movie.douban.com/j/chart/top_list?"
        self.query_dict = {
            "type": int(raw_input('电影类型:')),
            "interval_id": "100:90",
            "action": "",
            "start": int(raw_input('开始排名:')),
            "limit": int(raw_input("电影数量:")),
        }

    def send_request(self):
        query_str = urllib.urlencode(self.query_dict)
        url = self.url_prefix + query_str
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)
        json_data = response.read()

        return json_data

if __name__ == '__main__':
    rank = DoubanRank()
    json_data = rank.send_request()
    dict_data = json.loads(json_data)

    for ele in dict_data:
        print(ele['title'].encode('utf-8'))
