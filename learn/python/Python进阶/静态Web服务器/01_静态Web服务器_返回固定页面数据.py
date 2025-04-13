import socket
import threading

if __name__ == '__main__':
  
# 1. 编写一个TCP服务端程序
  # 1.创建TCP服务端套接字
  tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcp_socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  # 2.绑定IP地址和端口号
  tcp_socket_server.bind(('127.0.0.1', 8080))
  # 3.设置监听，等待客户端连接
  tcp_socket_server.listen(128)

  while True:
# 2. 获取浏览器发送的HTTP请求报文数据
    # 1.建立连接
    client_socket, client_addr = tcp_socket_server.accept()
    # 2.获取浏览器请求信息
    client_request_data = client_socket.recv(1024).decode()
    # 3.打印
    print(client_request_data)

# 3. 读取固定页面数据，把页面数据组装成HTTP响应报文数据发送给浏览器
    with open('learn\Python进阶\static\品优购项目\index.html', 'rb') as f:
      file_data = f.read()

    # 应答行
    response_line = 'HTTP/1.1 200 OK\r\n'
    # 应答头
    response_header = 'Server: Python\r\n'
    # 应答体
    response_body = file_data
    # 组装HTTP响应报文数据
    response_data = (response_line + response_header + '\r\n').encode() + response_body

    client_socket.send(response_data)
    
# 4. HTTP响应报文数据发送完成以后，关闭服务于客户端的套接字
    client_socket.close()

    

