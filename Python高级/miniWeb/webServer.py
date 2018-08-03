from socket import *
import re
import gevent
from gevent import monkey
import sys

monkey.patch_all()


class WebServer(object):
    def __init__(self, port, application):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.port = port
        self.tcpSocket.bind(("", port))
        self.tcpSocket.listen(128)
        self.application = application

    def start(self):
        while True:  
            severSocket, clientAddr = self.tcpSocket.accept()
            gevent.joinall([gevent.spawn(self.__handleData, severSocket)])

    def start_response(self, status, response_headers):
        self.status = status
        self.response_headers = response_headers

    def __handleData(self, severSocket):
        recvData = severSocket.recv(2048).decode()
        if len(recvData) == 0:  
            print("断开连接")
            severSocket.close()
            return
        else:
            recvLines = recvData.splitlines()
            firstLine = recvLines[0]
            keyWord = re.match(r"([^/]*)([^ ]*)", firstLine).group(2)

            if keyWord.endswith(".html"):
                # 请求伪静态网页
                env = {"PATH_INFO": keyWord}
                response_body = self.application(env, self.start_response)
                response_header = "HTTP/1.1 %s \r\n"
                for line in self.response_headers:
                    s1, s2 = line
                    response_header += "%s:%s\r\n" % (s1, s2)
                response_header += "\r\n"
                response_header += response_body
                severSocket.send(response_header.encode())
            else:
                # 请求静态网页
                fileName = "static" + keyWord
                if keyWord == "/":  
                    with open("templates/index.html", "rb") as g:
                        indexHtml = g.read()
                    severSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                    severSocket.send(indexHtml)
                else:
                    try: 
                        with open(fileName, "rb") as f:
                            content = f.read()
                    except Exception as _:  
                        content = "404 Not Found".encode()
                        severSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                        severSocket.send(content)
                    else:  
                        severSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                        severSocket.send(content)
        severSocket.close()

    def __del__(self):
        self.tcpSocket.close()


def main():
    # 程序入口
    if len(sys.argv) < 3:
        print("请指定端口：")
    port = int(sys.argv[1])
    moudle_method_name = sys.argv[2]
    ret = moudle_method_name.split(":")
    moudle_name = ret[0]
    method_name = ret[1]
    sys.path.insert(0, "./dynamic")
    webFramework = __import__(moudle_name)
    application = getattr(webFramework, method_name)
    miniWeb = WebServer(port, application)
    miniWeb.start()


if __name__ == '__main__':
    main()
