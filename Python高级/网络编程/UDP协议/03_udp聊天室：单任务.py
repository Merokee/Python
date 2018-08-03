# 创建套接字，指定端口
# 定义发送函数
# 定义接收函数
# 选择功能
# 关闭套接字
import socket

def sendMsg(udp):
    # 发送信息
    msg = input("发送信息：")
    aimIp = str(input("ip:"))
    aimPort = int(input("port:"))
    aimAddr = (aimIp, aimPort)
    udp.sendto(msg.encode("gbk"), aimAddr)

def recvMsg(udp):
    # 接收信息
    recvData = udp.recvfrom(1024)
    content, oppAddr = recvData
    print(content.decode("gbk"))
    return oppAddr

def comunicate(udp, oppAddr):
    msg = input("发送信息：")
    udp.sendto(msg.encode("gbk"), oppAddr)

def main():
    while True:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(("192.168.40.72", 3030))
        ctrlNum = input("功能选择：1，发送信息：2，接收信息")
        if ctrlNum == "1":
            sendMsg(udp)
        elif ctrlNum == "2":
            oppAddr = recvMsg(udp)
            num = input("回复请按1，退出请按2")
            if num == "1":
                comunicate(udp, oppAddr)
            elif num == "2":
                continue
        udp.close()
        
if __name__ ==  "__main__":
    main()
