from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.firefox.options import Options


def search_and_book(bro, train_numbers, seat_type):
    # bro.refresh()
    # page_text = bro.page_source
    # with open("./train.html", "w") as f:
    #     f.write(page_text)
    i = 0
    train_rows = bro.find_elements(By.XPATH, '//tbody[@id="queryLeftTable"]/tr[@id[starts-with(.,"ticket")]]')
    print(f"找到{len(train_rows)}趟次")
    while True:
        # bro.refresh()
        try:
            train_rows = bro.find_elements(By.XPATH, '//tbody[@id="queryLeftTable"]/tr[@id[starts-with(.,"ticket")]]')
            if i >= len(train_rows):
                return
            while i < len(train_rows):
                try:
                    train_row = train_rows[i]
                    train_number_element = train_row.find_element(By.XPATH, './/a[@class="number"]')
                    train_number = train_number_element.text.strip()
                    if train_number not in train_numbers:
                        i += 1
                        continue
                    # train_row_html = train_row.get_attribute("outerHTML")
                    # with open("./train_row.html", "w") as f:
                    #     f.write(train_row_html)
                    check_element = train_row.find_element(By.XPATH, f'.//td[@id[starts-with(.,"{seat_type}")]]')
                    check = check_element.text.strip()
                    id = train_row.get_attribute('id')
                    if check not in ["--", "无"]:
                        book = bro.find_element(By.XPATH, f'//tr[@id="{id}"]//a[@class="btn72"]')
                        bro.execute_script("arguments[0].click();", book)
                        sleep(1)
                        print(f"{train_number}抢票成功！")
                        try:
                            book_confirm = bro.find_element(By.XPATH,
                                                            '//*[@id="qd_closeDefaultWarningWindowDialog_id"]')
                            bro.execute_script("arguments[0].click();", book_confirm)

                        except Exception as e:
                            pass
                            print("没有确认框")
                            # print(f"确认预定错误:{e}")
                        sleep(3)
                        bro.back()
                        sleep(3)
                        bro.refresh()
                        i += 1
                        break
                    else:
                        i += 1
                        print(f"无票，{train_number}抢票失败！")
                        sleep(3)
                except Exception as e:
                    print("处理车次行出错！", e)

        except Exception as e:
            print("获取车次信息出错！", e)


if __name__ == "__main__":
    # 获取网页
    bro = webdriver.Chrome()
    bro.get("https://www.12306.cn/index/")
    # 登陆
    login_button = bro.find_element(By.XPATH, '//*[@id="J-btn-login"]')
    login_button.click()

    scan_btn = bro.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/ul/li[2]/a')
    scan_btn.click()

    # username = bro.find_element(By.XPATH, '//*[@id="J-userName"]')
    # username.send_keys("18902249719")
    # sleep(2)
    # password = bro.find_element(By.XPATH, '//*[@id="J-password"]')
    # password.send_keys("mg20010818")
    # sleep(2)
    # btn = bro.find_element(By.XPATH, '//*[@id="J-login"]')
    # btn.click()
    # code = bro.find_element(By.XPATH, '//*[@id="id_card"]')
    # code.send_keys("0612")
    # get_captcha = bro.find_element(By.XPATH, '//*[@id="verification_code"]')
    # get_captcha.click()
    # 验证码
    input("扫码了吗？")
    # input_captcha = bro.find_element(By.XPATH, '//*[@id="code"]')
    # input_captcha.send_keys(CAPTCHA)
    # sleep(2)
    # confime_btn = bro.find_element(By.XPATH, '//*[@id="sureClick"]')
    # confime_btn.click()
    sleep(5)
    # 购票
    main_page_btn = bro.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/ul/li[1]/a')
    main_page_btn.click()
    sleep(1)
    src = bro.find_element(By.XPATH, '//*[@id="fromStationText"]')
    src.click()
    src.send_keys("广州南")
    sleep(1)
    src.send_keys(Keys.ENTER)
    sleep(1)
    dst = bro.find_element(By.XPATH, '//*[@id="toStationText"]')
    sleep(1)
    dst.send_keys("衡阳")
    sleep(1)
    dst.send_keys(Keys.ARROW_DOWN)
    sleep(1)
    dst.send_keys(Keys.ENTER)
    sleep(1)
    click_student = bro.find_element(By.XPATH,
                                     '/html/body/div[1]/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div[3]/div/ul/li[1]/i')
    click_student.click()
    sleep(1)
    search_btn = bro.find_element(By.XPATH, '//*[@id="search_one"]')
    search_btn.click()

    train_numbers = []
    print("请输入车次（按回车键结束输入）：")
    i = 1
    while True:
        val = input(f"第{i}个车次为")
        if val == "":
            break
        train_numbers.append(val.strip())
        i = i + 1
    all_windows = bro.window_handles
    bro.switch_to.window(all_windows[1])
    sleep(2)
    bro.back()
    sleep(1)
    bro.forward()
    sleep(1)
    search_and_book(bro, train_numbers, "YW")

    sleep(5)
    bro.quit()