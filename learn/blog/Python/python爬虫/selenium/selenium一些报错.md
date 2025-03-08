### 使用selenium自动化爬虫过程中 Message: Tried to run command without establishing a connection

~~~python
大概率是driver.close()了
注意在只剩下最后一个窗口时，driver.close()会直接关掉浏览器
~~~



###   subprocess.Popen('"D:\\tor\Tor Browser\Browser\\firefox.exe"  --marionette --marionette-port 2828')			geckodriver.exe: error: 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。 (os error 10048)

~~~python
geckodriver端口占用未关闭
netstat -ano|findstr "4444" netstat -ano|findstr "2828" 监听端口，找到占用，后面的数字是PID
打开任务管理器，关闭进程即可
~~~

