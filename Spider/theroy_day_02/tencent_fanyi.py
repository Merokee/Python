# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-9 下午7:51
import urllib, urllib2, time, json


def translate():
    # 获取url时注意是否必需为https
    url = 'https://fanyi.qq.com/api/translate'

    form_dict = {
        "source": "auto",
        "target": "auto",
        "sourceText": raw_input('要翻译的内容：'),
        "sessionUuid": "translate_uuid" + str(int(time.time()*1000)),
    }
    form_data = urllib.urlencode(form_dict)

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": len(form_data),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "pgv_pvi=2875190272; RK=BjLkFMXFeO; ptcz=1e482d8c194d435f3d60e6214d8dd77571a0960d4f932ae00d0c4a9ea033aad7; pgv_pvid=7068101000; ptui_loginuin=1401065276; pt2gguin=o1401065276; fy_guid=f27dd22f-0e64-4b57-84f1-a0822858987a; qtv=0107bec9a3452c97; qtk=1l9YS0Iy5zX2PcV8PYSnx5mTrd6brwOqpvF9r2t9kJQagesltzywp9tlOlXeLPNC+qwLh0gFLMI29NfKkZSRO9OQNNt97DB93dTJZrKqNXgflCzWxhSynW4pCB4E7Uh3WfIezD4VRVRxg3kt0RY4dQ==; pgv_info=ssid=s4070710256; ts_last=fanyi.qq.com/; ts_refer=www.sogou.com/link; ts_uid=2048501051; openCount=1",
        "Host": "fanyi.qq.com",
        "Origin": "https://fanyi.qq.com",
        "Referer": "https://fanyi.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        # "X-Requested-With": "XMLHttpRequest",
    }

    request = urllib2.Request(url, form_data, headers)
    response = urllib2.urlopen(request)
    return response.read()


if __name__ == '__main__':
    json_content = translate()
    dict_content = json.loads(json_content)
    print(dict_content['translate']['records'][0]['targetText'])
