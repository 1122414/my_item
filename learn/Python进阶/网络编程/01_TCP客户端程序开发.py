import socket

if __name__ == '__main__':
  # 1.创建客户端套接字对象
    # AF_INET:使用IPv4协议
    # SOCK_STREAM:使用TCP协议
  tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

  # 2.和服务端套接字建立连接
  tcp_client_socket.connect(('192.168.19.1',8080))

  # 3.发送数据
  tcp_client_socket.send("Hello".encode(encoding='utf-8'))

  # 4.接收数据  recv阻塞等待数据的到来
  recv_data = tcp_client_socket.recv(1024)

  # 关闭客户端套接字
  tcp_client_socket.close()
  print(recv_data.decode('utf-8'))