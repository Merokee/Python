"""
返回静态和伪静态网页
终端执行，并在终端中导入框架和接口
"""
'''GET / HTTP/1.1
Host: 127.0.0.1:8898
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
'''

import socket, sys, re, gevent
from gevent import monkey


monkey.patch_all()


class WebServer:
    def __init__(self, port, application):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpSocket.bind(("", port))
        self.tcpSocket.listen(128)
        self.app = application

    def startResponse(self, status, headers):
        self.status = status
        self.headers = headers

    def handleData(self, serverSocket):
        recvMsg = serverSocket.recv(2048)
        if not recvMsg:
            print("断开链接")
            serverSocket.close()
            return
        firstLine = recvMsg.decode("utf-8").splitlines()[0]
        fileName = re.match(r"[^/]*([^ ]*)", firstLine).group(1)
        print(fileName)
        responseMsg = "HTTP/1.1 200 OK\r\n\r\n"
        if fileName.endswith(".html"):
            env = {"PATH_INFO": fileName}
            response_body = self.app(env, self.startResponse)
            responseMsg = "HTTP/1.1 " + self.status + "\r\n"
            for header in self.headers:
                responseMsg += "%s:%s\r\n" % (header[0], header[1])
            responseMsg += "\r\n" + response_body
            print(responseMsg)
            print("**"*50)
        else:
            if fileName == "/":
                with open("templates/index.html", "r") as f:
                    content = f.read()
                    responseMsg += content
            else:
                try:
                    with open("static" + fileName, "r") as g:
                        content = g.read()
                except Exception as _:
                    responseMsg = "HTTP/1.1 404 NotFound\r\n\r\n"
                    responseMsg += "404 File Not Found"
                else:
                    responseMsg += content
        serverSocket.send(responseMsg.encode("utf-8"))
        serverSocket.close()

    def start(self):
        while True:
            serverSocket, clientAddr = self.tcpSocket.accept()
            print(clientAddr, "链接成功")
            gevent.spawn(self.handleData, serverSocket)


def main():
    if len(sys.argv)<3:
        print("请输入端口和框架接口")
    framework_app = sys.argv[2].split(":")
    framework_name, app_name = framework_app[0], framework_app[1]
    sys.path.insert(0, "dynamic")
    framework = __import__(framework_name)
    application = getattr(framework, app_name)
    port = int(sys.argv[1])
    server = WebServer(port, application)
    server.start()


if __name__ == '__main__':
    main()