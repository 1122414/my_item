from selenium import webdriver
from selenium.webdriver.common.by import By
# 导入动作链对应的类
from selenium.webdriver import ActionChains
from time import sleep

bro = webdriver.Chrome()
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

# 如果定位的标签是存在于iframe标签之中的则必须通过如下操作再进行标签定位
# 先切换到iframe标签，作用域指定
bro.switch_to.frame('iframeResult')
div = bro.find_element(By.ID, 'draggable')
# 动作链
action = ActionChains(bro)
# 点击长按指定标签
action.click_and_hold(div)
# perform()方法执行动作链
# (x,y)
for i in range(5):
  action.move_by_offset(17,0).perform()
  sleep(0.5)
# 关闭动作链
action.release().perform()

sleep(2)
bro.quit()