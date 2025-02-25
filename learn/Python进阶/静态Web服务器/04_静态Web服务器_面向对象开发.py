import socket
import threading
  # # 3. 关闭服务端套接字
  # tcp_socket_server.close()

class HttpWebServer:
  def __init__(self) -> None:
  # 1. 编写一个TCP服务端程序
    # 1.创建TCP服务端套接字
    self.tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp_socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    # 2.绑定IP地址和端口号
    self.tcp_socket_server.bind(('127.0.0.1', 8080))
    # 3.设置监听，等待客户端连接
    self.tcp_socket_server.listen(128)
    pass

  def solve_request(self,status_code,client_socket, client_addr, file_data):
  # 应答头
    response_header = 'Server: Python\r\n'
    if status_code == 200:
      # 应答行
      response_line = 'HTTP/1.1 200\r\n'
      # 应答体
      response_body = file_data
      # 组装HTTP响应报文数据
      response_data = (response_line + response_header + '\r\n').encode() + response_body

    elif status_code == 404:
      # 应答行
      response_line = 'HTTP/1.1 404 Not Found\r\n'
      # 应答体
      response_body = "404 Not Found"
      # 组装HTTP响应报文数据
      response_data = (response_line + response_header + '\r\n' + response_body).encode() 
    client_socket.send(response_data)

  def handle_client(self,client_socket, client_addr):
  # 2.获取浏览器请求信息
    client_request_data = client_socket.recv(1024).decode()
    # 3.打印
    print(client_request_data)
    
    # 4.获取用户请求资源路径
    request_data = client_request_data.split()

    # 判断客户端是否关闭
    if len(request_data)==1:
      client_socket.close()
      return
    print(request_data)
    request_path = request_data[1]
    if request_path == "/":
        request_path = "/index.html"

  # 3. 读取固定页面数据，把页面数据组装成HTTP响应报文数据发送给浏览器
    try:
      with open(f'learn\Python进阶\static\品优购项目\{request_path}', 'rb') as f:
        file_data = f.read()
    except Exception as e:
      self.solve_request(404, client_socket, client_addr, None)
    else:
      self.solve_request(200, client_socket, client_addr, file_data)
      
    finally:
  # 4. HTTP响应报文数据发送完成以后，关闭服务于客户端的套接字
      client_socket.close()

  def start(self):
    while True:
# 2. 获取浏览器发送的HTTP请求报文数据
    # 1.建立连接
      client_socket, client_addr = self.tcp_socket_server.accept()
      sub_thread = threading.Thread(target=self.handle_client,args=(client_socket,client_addr,))
      sub_thread.start()

if __name__ == '__main__':
  # 创建服务器对象
  my_web_server = HttpWebServer()
  # 启动服务器
  my_web_server.start()