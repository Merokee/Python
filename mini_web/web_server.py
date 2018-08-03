import socket
import re
import sys
import gevent
from gevent import monkey


monkey.patch_all()

g_static_root = './static'

class WebServer(object):
    def __init__(self, port,app):
        # 1. 创建套接字
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 套接字端口复用
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定本地信息
        self.port = port
        self.tcpSocket.bind(("", self.port))
        print("服务器绑定端口为：", self.port)

        self.response_status_header = ""
        # 3. 设置为监听套接字
        self.tcpSocket.listen(128)
        self.app = app

    def StartUp(self):
        while True:
            # 4. 等待新的客户端链接
            clientSocket, clientAddr = self.tcpSocket.accept()
            print(clientAddr, "连接成功")
            
            # 5. 为这个客户端服务
            # 创建这个对象之后，gevent就知道了当遇到耗费时间的时候可以切换到这个对象指定的函数中运行
            gevent.spawn(self.serviceClient, clientSocket) 

        # 6. 关闭套接字
        self.tcpSocket.close()
        
    
    def serviceClient(self, clientSocket):
        """为客户端服务"""
        # 1. 接收客户端发送过来的http的请求数据
        request =  clientSocket.recv(1024).decode("utf-8")
        print(">"*40, "\n", request)
        if not request:
            return
        
        # 以行为单位切割，并返回一个列表
        requestLines = request.splitlines()
        print("====>", requestLines)
        
        # GET /index.html HTTP/1.1
        requestFirstLine = requestLines[0]
        
        # 通过正则表达式提取相应的文件名
        fileName = re.match(r"[^/]+(/[^ ]*)", requestFirstLine).group(1)
        
        # 如果后面没有路径，默认是index.html
        if fileName == "/":
            fileName = "/index.html"
        
        print("-----请求的文件名是：%s" % fileName)
        # 如果是以html结尾的就是动态资源
        if fileName.endswith(".html"):
            # 动态资源 交给web框架完成业务处理
            env = {"PATH_INFO":fileName}
            body = self.app(env, self.start_response)
            data = self.response_status_header + body
            clientSocket.send(data.encode())
            clientSocket.close()
        else:
            # 静态资源
            # 3. 根据文件名去读取这个文件的内容，如果有就发送，如果没有就告诉浏览器 这个资源不存在404
            try:
                with open(g_static_root + fileName, "rb") as f:
                    content = f.read()
            except Exception as ret:
                # 意味着没有这个请求的资源  404
                # 返回http的应答数据
                responseHeader  = "HTTP/1.1 404 NOT FOUND\r\n"
                responseHeader += "\r\n"
                responseBody = "------file not found-------".encode("utf-8")
            else:
                # 意味着 有这个对应的资源 200
                # 返回http的应答数据
                responseHeader  = "HTTP/1.1 200 OK\r\n"
                responseHeader += "\r\n"
                responseBody = content


            # 返回http的应答数据
            clientSocket.send(responseHeader.encode("utf-8")) #先发头
            clientSocket.send(responseBody) #先发body

            # 4. 关闭套接字
            clientSocket.close()

    def start_response(self,status, response_headers):
        print("程序执行到start_response")
        self.response_status_header = "HTTP/1.1 %s\r\n" % status
        for name, value in response_headers:
            self.response_status_header += ("%s:%s\r\n" % (name, value))

        self.response_status_header += "\r\n"



def main():
    if len(sys.argv) < 3:
        print('您需要指定监听端口!')
        return

    # 获取用户指定的绑定端口
    port = int(sys.argv[1])
    module_name = sys.argv[2]
    module = __import__(module_name)
    application_method = getattr(module,"application")
    print(application_method)

    # 创建服务器
    server = WebServer(port,application_method)
    
    # 启动服务器
    server.StartUp()


    
if __name__ == "__main__":
    main()

