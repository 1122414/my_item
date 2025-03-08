适当更改此命令

```python
pyinstaller -F --add-data "./my_selenium_utils;my_selenium_utils"  --hidden-import=selenium.webdriver.common.by  --hidden-import=selenium.webdriver.common.action_chains  --hidden-import=moviepy.editor  --hidden-import=pymysql  --hidden-import="pkg_resources" --hidden-import="pkg_resources.extern" --hidden-import="pkg_resources.py31compat" --name "哔站视频下载器"  main.py
```
