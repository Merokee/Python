# 创建套接字
# 发送数据
# 固定端口
# 接收对方回复
# 关闭套接字
import socket

# 创建套接字

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 固定端口
udp.bind(("192.168.40.72", 7070)) 

# 发送数据

addr = ("192.168.40.54", 8080)
info = input("发送：")
udp.sendto(info.encode("gbk"), addr)

# 接收对方并自动回复

recvData = udp.recvfrom(1024)
content, oppAddr = recvData
udp.sendto("对方正在开会没空和你bb！".encode("gbk"), oppAddr)
print("recvData= ", content.decode("gbk"))

# 关闭套接字

udp.close()
