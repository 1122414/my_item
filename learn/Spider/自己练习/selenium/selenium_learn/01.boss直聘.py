
from lxml import etree
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.zhipin.com/job_detail/?query=Python%E5%BC%80%E5%8F%91&city=100010000")
# 等待页面加载完成
sleep(15)

job_name_list = driver.find_elements(By.XPATH, '//span[@class="job-name"]')
job_area_list = driver.find_elements(By.XPATH, '//span[@class="job-area"]')
job_salary_list = driver.find_elements(By.XPATH, '//span[@class="salary"]')
for i in range(len(job_name_list)):
    job_name = job_name_list[i].text
    job_area = job_area_list[i].text
    job_salary = job_salary_list[i].text
    print(f"职位名称：{job_name}\n工作地点：{job_area}\n薪资：{job_salary}\n")

input("Press any key to quit...")