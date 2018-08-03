# 导包
import socket
# 创建tcp套接字
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 拨号
tcp.connect(("192.168.40.38", 8080))
# 发送数据
tcp.send("轻轻贴近你的耳朵，沙拉嘿呦".encode("gbk"))
# 接收数据
recvData = tcp.recv(1024)
print(recvData)
# 关闭套接字
tcp.close()
