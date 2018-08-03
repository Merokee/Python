from socket import *
import re


def handleData(severSocket):
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
        print("请求关键字：", keyWord)
        fileName = "html" + keyWord
        if keyWord == "/":
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


def main():
    # 程序入口
    # 创建监听套接字
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    # 端口复用
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定端口
    tcpSocket.bind(("", 8888))
    # 监听
    tcpSocket.listen(128)
    # 接收服务套接字
    while True:
        severSocket, clientAddr = tcpSocket.accept()
        print(clientAddr, ">>已连接！<<")
        handleData(severSocket)
    # 关闭监听套接字
    tcpSocket.close()
    print("关闭监听套接字！")


if __name__ == '__main__':
    main()