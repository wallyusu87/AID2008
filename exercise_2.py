
from socket import *

s = socket()
s.bind(("0.0.0.0",8880))
s.listen(5)

c,addr = s.accept() # 浏览器连接
print("Connect from",addr)

# 接收浏览器发送的HTTP请求
data = c.recv(1024 * 10).decode()
tmp = data.split(" ")
# 判断请求内容
if tmp[1] == "/python":
    with open("Python.html") as f:
        content = f.read()
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += content
else:
    response = "HTTP/1.1 404 Not Found\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += "Sorry..."

# 发送响应
c.send(response.encode())

c.close()
s.close()



