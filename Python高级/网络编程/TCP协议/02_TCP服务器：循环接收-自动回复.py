import socket
# 创建TCP套接字
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口
tcp.bind(("", 8888))
# 等待连接
tcp.listen(128)
while True:
    # 分配服务
    severSocket, Addr = tcp.accept()
    # 循环接收数据
    while True:
        recvData = severSocket.recv(1024)
        print(recvData.decode("gbk"))
        if recvData is None:
            break
    # 发送信息
    severSocket.send("对方不想和你说话，并给了你一耳巴子！".encode("gbk"))
    severSocket.close()
# 关闭套接字
tcp.close()
