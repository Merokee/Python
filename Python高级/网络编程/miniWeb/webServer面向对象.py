from socket import *
import re
import gevent
from gevent import monkey


# 打补丁，耗时自动切换任务
monkey.patch_all()


class WebServer(object):
    def __init__(self):
        # 创建监听套接字
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 端口复用
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 绑定端口
        self.tcpSocket.bind(("", 8888))
        # 监听
        self.tcpSocket.listen(128)

    def start(self):
        while True:  # 持续接收客户端请求
            severSocket, clientAddr = self.tcpSocket.accept()
            gevent.joinall([gevent.spawn(self.__handleData, severSocket)])
    def __handleData(self, severSocket):
        # 接收数据
        recvData = severSocket.recv(2048).decode()
        if len(recvData) == 0:  # 当客户端断开链接时关闭服务套接字
            print("断开连接")
            severSocket.close()
            return
        else:
            # 取出请求报文的第一行
            recvLines = recvData.splitlines()
            firstLine = recvLines[0]

            # 用正则表达式取出关键字
            keyWord = re.match(r"([^/]*)([^ ]*)", firstLine).group(2)
            fileName = "html" + keyWord

            # 判断服务器是否有请求的目标网页
            if keyWord == "/":  # 即请求行："GET / HTTP/1.1"
                # 返回固定网页
                with open("html/index.html", "rb") as g:
                    indexHtml = g.read()
                severSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                severSocket.send(indexHtml)
            else:
                try:  # 判断是否有目标网页，没有则抛出FileNotFound异常
                    with open(fileName, "rb") as f:
                        content = f.read()
                except Exception as _:  # 捕捉到异常信息，返回404 Not Found响应报文
                    content = "404 Not Found".encode()
                    severSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    severSocket.send(content)
                else:  # 未捕捉到异常，发送目标响应报文
                    severSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                    severSocket.send(content)
        # 关闭套接字
        severSocket.close()

    def __del__(self):
        # 关闭监听套接字
        self.tcpSocket.close()


def main():
    # 程序入口
    miniWeb = WebServer()
    miniWeb.start()


if __name__ == '__main__':
    main()
