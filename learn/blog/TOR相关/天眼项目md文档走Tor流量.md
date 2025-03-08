1. setting中端口改成9150

2. privoxy的config最后一行加上

   ~~~
   forward-socks5t   /               127.0.0.1:9150 .
   ~~~

   