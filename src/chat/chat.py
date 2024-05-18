import time

from selenium.webdriver.common.by import By

from src import consts


# 聊天
def chat(driver):
    enter_chat_page(driver)
    # 等待页面加载完成
    time.sleep(3)
    for question in consts.CHAT_QUESTIONS:
        send_message(driver, question)
        print(get_reply(driver))


# 进入聊天界面
def enter_chat_page(driver):
    ice_container = driver.find_element(By.XPATH, '//div[@id="ice-container"]')
    iframe = ice_container.find_element(By.TAG_NAME, 'iframe')
    message_frame_url = iframe.get_attribute("src")
    driver.get(message_frame_url)


# 发送指定话术
def send_message(driver, message):
    # 输入话术
    edit_box = driver.find_element(By.XPATH, '//div[@class="editBox"]')
    pre_edit = edit_box.find_element(By.XPATH, '//pre[@class="edit"]')
    pre_edit.send_keys(message)

    # 查找发送按钮，并点击发送
    ww_input = driver.find_element(By.XPATH, '//div[@class="ww_input"]')
    send_button = ww_input.find_element(By.XPATH, "//button[@class='next-btn next-small next-btn-primary send-btn']")
    send_button.click()


def get_reply(driver):
    last_message = get_last_message_text(driver)
    times = 0
    # 循环监听最新的消息
    while (times + 1) <= consts.MAX_POLLING_TIMES:
        print("等待回复中，等待次数：{}".format(times + 1))
        current_message = get_last_message_text(driver)
        if current_message != last_message:
            return current_message
        time.sleep(consts.POLLING_WAIT_SECONDS)
        times += 1
    return consts.NO_REPLY_MESSAGE


def get_last_message_text(driver):
    message_list = driver.find_elements(By.XPATH, '//div[@class="message-item"]')
    if len(message_list) > 0:
        return message_list[-1].text
    return consts.NO_REPLY_MESSAGE
