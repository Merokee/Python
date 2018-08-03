from urllib import request
from urllib import parse
input_content = input("输入你想搜索的内容：")
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
query_dict = {"ie": "utf-8", "wd": input_content}
query_str = parse.urlencode(query_dict)
req = request.Request("https://www.baidu.com/s?"+query_str, headers=headers)
response = request.urlopen(req)
with open("baidu.Html", "wb") as f:
    f.write(response.read())
