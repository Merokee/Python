# miniWeb服务器
import socket, gevent, re, sys
from gevent import monkey

monkey.patch_all()


class webServer(object):
    def __init__(self, port, app):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpSocket.bind(("", port))
        self.tcpSocket.listen(128)
        self.app = app

    def start_response(self, status, response_headers):
        self.status = status
        self.response_headers = response_headers
        # print(self.status, self.response_headers)

    def handle_data(self):
        serverSocket, clientAddr = self.tcpSocket.accept()
        recvData = serverSocket.recv(2048)
        if len(recvData) == 0:
            serverSocket.close()
            print("断开连接")
            return
        lines_list = recvData.decode().splitlines()
        fist_line = lines_list[0]
        file_path = re.match(r"[^/]*([^ ]*)", fist_line).group(1)
        print("文件地址", file_path)
        if file_path.endswith(".html"):
            # 返回伪静态网页
            env = {"PATH_INFO":file_path}
            content = self.app(env, self.start_response)
            status_lines = "HTTP/1.1 %s \r\n" % self.status
            for element in self.response_headers:
                el1, el2 = element[0], element[1]
                status_lines += "%s:%s\r\n" % (el1, el2)
            status_lines += "\r\n" + content
            # print(status_lines)
            serverSocket.send(status_lines.encode())
             
        else:
            # 返回静态网页
            response_headers = "HTTP/1.1 200 OK\r\n\r\n"
            if file_path == "/":
                with open("./templates/index.html", "r") as f:
                    response_body = f.read()
                    # print(response_body)
                content = response_headers + response_body
                serverSocket.send(content.encode())
            file_path = "./static" + file_path
            try:
                with open(file_path, "r") as f:
                    response_body = f.read()
                content = response_headers + response_body
            except Exception:
                response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
                response_headers += "404 Not Found 文件未找到"
                serverSocket.send(response_headers.encode())
            else:
                serverSocket.send(response_headers.encode())
        serverSocket.close()

    def start(self):
        while True:
            g = gevent.spawn(self.handle_data)
            g.join()

        

def main():
    if len(sys.argv) < 3:
        print("参数不全")
    port = int(sys.argv[1])
    g_moudle_app_name = sys.argv[2].split(":")
    moudle_name, app_name = g_moudle_app_name[0], g_moudle_app_name[1]
    sys.path.insert(0, "./dynamic")
    moudle = __import__(moudle_name)
    app = getattr(moudle, app_name)
    server = webServer(port, app)
    server.start()

if __name__ == "__main__":
    main()
