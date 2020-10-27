"""
web server 程序

完成一个类，提供给使用者
可以通过这个类快速搭建服务
完成网页展示
"""
from socket import *
from select import select
import re

class WebServer:
    def __init__(self, host='0.0.0.0',port=80,html=None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()


    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host,self.port)
        self.sock.bind(self.address)


    def start(self):
        # 创建监听套接字
        self.sock.listen(5)
        print('Listen the port %d'%self.port)
        self.rlist.append(self.sock)

        # 创建IO并发模型
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            connfd,self.address = self.sock.accept()
            for r in rs:
                if r is self.sock:
                    connfd,addr = r.accept()
                    print('Connect from ',addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # 处理HTTP请求
                    self.handle(r)
                    self.rlist.remove(r)
                    r.close()

    def handle(self,connfd):
        # HTTP请求
        request = connfd.recv(1024 * 10)
        print(request)
        pattern = r"[A-Z]+\s+(?P<info>/\S*"
        result = re.match(pattern,request)
        if request:
            info = result.group('info')
            print('请求内容： ',info)
            self.send_html(connfd,info)

    def send_html(self, connfd, info):
        if info == '/':
            filename = self.html + '/index.html'
        else:
            filename = self.html + info

        try:
            file = open(filename,'rb')
        except:
            # 请求的网页不存在
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            with open(self.html + '/404.html','rb')


if __name__ == '__main__':
    # 创建实例化对象
    web_server = WebServer(host='0.0.0.0',port=8888,html='./static')

# 启动服务
web_server.start()
