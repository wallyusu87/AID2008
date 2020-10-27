"""
练习：编写一个程序完成，如果浏览器访问127.0.0.1:8888//python
的时候可以访问到python.html网页，否则
访问不到任何内容，得到404响应
"""

from socket import *

s = socket()
s.bind(('0.0.0.0', 8888))
s.listen(5)

c, addr = s.accept()
print('Connect from:', addr)
if addr == '127.0.0.1':
    f = open('Python.html','rb')
    # 接收浏览器发送的HTTP请求
    data = c.recv(1024 * 10)
    print(data.decode())
# 发送http响应给浏览器
response = f"""HTTP/1.1 200 OK
Content-Type:text/html

{f.read()}
"""
c.send(response.encode())

c.close()
s.close()