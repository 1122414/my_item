### selenium切换标签页操作

1. #### 查看当前标签页

   ~~~python
   current_window = driver.current_window_handle 
   ~~~

   

2. #### 返回当前会话中所有窗口的句柄。

    ~~~python
   all_window=driver.window_handles    
   ~~~

   

3. #### 切换driver指向

   ~~~python
   driver.switch_to.window(window)  
   ~~~

### selenium driver常用属性和方法

~~~python
driver.page_source	#当前标签页浏览器渲染之后的源代码
driver.current_url	#当前标签页的url
driver.close()      #关闭当前标签页，如果只有一个标签页则关闭浏览器
driver.quit()       #关闭浏览器
driver.forward()    #页面前进
driver.back()       #页面后退
driver.screen_show(image_name)		#页面截图
~~~

### xpath定位

~~~python
/div[contains(text(),'hello world!')]	#包含hello world!的div
~~~





1. 惊叹fly
2. 飞电4c
3. 乔丹PB4   惊叹2跟3/4差不多
4. 飞电4E
5. 乔丹plaid