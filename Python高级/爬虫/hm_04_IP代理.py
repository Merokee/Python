"""设置代理"""
from urllib import request
from urllib import parse
# 普通代理：{“协议”：“代理IP:代理端口号”}
# 授权代理：{“协议”：“账号名：密码@代理IP:代理端口号”}
proxy_dict = {"http": "zhangzz7998:ykqnd5kh@121.42.148.121:16816"}
handler = request.ProxyHandler(proxy_dict)
opener = request.build_opener(handler)
# 设置全局代理

# input_content = input("输入你行搜索的内容：")
# headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
#                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
# query_dict = {"ie": "utf-8", "wd":input_content}
# query_str = parse.urlencode(query_dict)
# request.install_opener(opener)
# req = request.Request("https://www.baidu.com/s?"+query_str, headers=headers)
# response = request.urlopen(req)
response = request.urlopen("http://www.httpbin.org/ip")
print(response.read())
# with open("daili.Html", "wb") as f:
#     f.write(response.read())