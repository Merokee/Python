# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午7:51
import urllib, urllib2, time, json, hashlib, random


def generate_sign():
    S = "fanyideskweb"
    n = raw_input("要翻译的内容")
    r = str(int(time.time()) + random.randint(0, 10))
    D = "ebSeFb%=XZ%T[KZ)c(sy!"
    sign = hashlib.md5(S + n + r + D).hexdigest()  # 转为16进制
    return n, S, r, sign


def translate():

    n, S, r, sign = generate_sign()
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    form_dict = {
        "i": n,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": S,
        "salt": r,
        "sign": sign,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
        "typoResult": "false",
    }
    form_data = urllib.urlencode(form_dict)

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": len(form_data),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID_NCOO=1730396188.6893692; OUTFOX_SEARCH_USER_ID=-1551664308@10.168.8.63; JSESSIONID=aaaK9l13NKwsz-WfHa-rw; fanyi-ad-id=46607; fanyi-ad-closed=1; ___rl__test__cookies=1531139694687",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        # "X-Requested-With": "XMLHttpRequest",
    }

    request = urllib2.Request(url, form_data, headers)
    response = urllib2.urlopen(request)
    return response.read()


if __name__ == '__main__':
    json_content = translate()
    dict_content = json.loads(json_content)

    print(dict_content['translateResult'][0][0]['tgt'])


