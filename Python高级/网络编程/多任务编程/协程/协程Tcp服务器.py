# 能收能发但是不能实现及时接收
import gevent
from gevent import monkey
from socket import *
import time


monkey.patch_all()


def recv(severSocket):
    while True:
        recvMsg = serverSocket.recv(1024).decode()
        print(recvMsg)
        time.sleep(2)


def send(severSocket):
    while True:
        msg = input("回复：").encode()
        time.sleep(2)


#定义一个主函数
tcp = socket(AF_INET, SOCK_STREAM)
tcp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcp.bind(("", 6666))
tcp.listen(128)
serverSocket, clientAddr = tcp.accept()
print("链接完成：", clientAddr)
gevent.joinall([gevent.spawn(recv, serverSocket), gevent.spawn(send, serverSocket)])
