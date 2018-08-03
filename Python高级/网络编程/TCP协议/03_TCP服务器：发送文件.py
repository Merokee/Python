from socket import *
import os
import time

# 创建套接字，绑定服务器ip/port
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(("", 5957))

# 监听客户端连接信号
tcp.listen(128)

# 分配服务套接字
severSocket, clientAddr = tcp.accept()
print(clientAddr,"连接成功！")
    
while True:
# 接收客户端需求
    print("---接收数据----")
    recvData = severSocket.recv(1024)
    fileName = recvData.decode()
    if fileName == "exit" or fileName is None:
        break
    print("客户端要下载的文件：%s" % fileName)
    if os.path.exists(fileName):
        with open(fileName, "rb") as f:
            while True:
                msg = f.readline() 
                if msg:
                    severSocket.send(msg)
                    print("发送成功！" + msg.decode())
                    time.sleep(0.1)
                else:
                    severSocket.send("exit".encode())
                    break
    else:
        severSocket.send("服务器无你请求的文件！".encode())
severSocket.close()

# 关闭套接字
tcp.close()
