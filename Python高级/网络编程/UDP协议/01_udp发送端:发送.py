import socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("192.168.40.81", 8080)
buf = "hey,man."
udp.sendto(buf.encode(), addr)
udp.close()
