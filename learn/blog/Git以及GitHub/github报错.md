## github常见报错

### 报错403

clash verge开了tun模式之后，可能是更改了某些东西

**解决：**

~~~bash
# 设置 HTTP/HTTPS 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
# 还是不是很清楚什么原因
~~~



