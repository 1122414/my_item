~~~python
import os
#	获取当前文件文件夹名称
current_path = os.path.dirname(os.path.abspath(__file__))
#	获取上一层级
farther_path = os.path.dirname(current_path)
~~~

![image-20240927104933594](img/image-20240927104933594.png)

1. /Python_code
2. /逆向