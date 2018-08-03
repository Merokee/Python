import time
from urllib import request
import random
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
req = request.Request("https://www.renren.com", headers= headers)
USER_AGENT_LIST = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"]
for _ in range(10):
    req.add_headers = random.choice(USER_AGENT_LIST)
    response = request.urlopen(req)
    print(response)
    time.sleep(5)



# from urllib import request
# import random
# with open("User-Agent-list.txt", "r") as f:
#     USER_AGENT_LIST = eval(f.read())
#
#
# class RequestHeaders:
#     def __init__(self, url):
#         # self.headers = {"User-Agent": random.choice(USER_AGENT_LIST)}
#         self.headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
#         self.url = url
#
#     def response(self):
#         req = request.Request(self.url, headers=self.headers)
#         response = request.urlopen(req)
#         return response
#
#     def write_file(self):
#         with open("demo.html", "wb") as g:
#             g.write(self.response().read())
#
# if __name__ == '__main__':
#     request_headers = RequestHeaders("http://www.baidu.com")
#     request_headers.write_file()

