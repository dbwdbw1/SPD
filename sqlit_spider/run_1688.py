import sys
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from consts import DEFAULT_1688_URL_PREFIX, LOGIN_URL_PREFIX
from sqlit_spider.sqlite3_model import SessionContext, GoodsInfo


def driver_init():
    # 加载配置数据
    profile_dir = r'--user-data-dir=C:\Users\hjl\AppData\Local\Google\Chrome\User Data'
    c_option = webdriver.ChromeOptions()
    c_option.add_experimental_option('useAutomationExtension', False)
    c_option.add_experimental_option('excludeSwitches', ['enable-automation'])

    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            },
        'profile.password_manager_enabled': False,
        'credentials_enable_service': False
    }
    c_option.add_experimental_option('prefs', prefs)

    # 开发者模式防止被识别出
    # 网址：https://blog.csdn.net/dslkfajoaijfdoj/article/details/109146051
    c_option.add_experimental_option('excludeSwitches', ['enable-automation'])
    c_option.add_argument("--disable-blink-features=AutomationControlled")
    # c_option.add_experimental_option('w3c', False)

    c_option.add_argument(profile_dir)
    driver = webdriver.Chrome(chrome_options=c_option)
    # 执行cdp命令
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                  """
    })

    return driver


# 打开链接获取商品的详细信息
def get_goods_detail(driver, link, original_window):
    while True:
        try:
            # 打开新窗口
            driver.execute_script("window.open('" + link + "')")
            # 等待浏览器加载完毕
            driver.implicitly_wait(7)
            # 获取所有窗口句柄
            all_handles = driver.window_handles
            goods_detail_handle = ''
            # 切换到新窗口
            for handle in all_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    goods_detail_handle = handle
                    break
            time.sleep(2)
            aliwangwang_button = driver.find_element(By.XPATH, "//a[@target='_blank' and @class='tool-item']")
            # 先点击展开按钮
            try:
                driver.find_element(By.CLASS_NAME, 'offer-attr-switch').click()
            except:
                pass
            time.sleep(1)

            try:
                # 获取商品信息
                goods_div = driver.find_elements(By.XPATH,
                                                 '//div[@class="offer-attr-list"]/div[@class="offer-attr-item"]')
            except Exception as e:
                print('商品信息解决出错，link:', link, 'err: ', e)
                goods_div = []
            try:
                # 获取地址信息
                address_div = driver.find_element(
                    By.XPATH,
                    '//div[@id="shop-container-footer"]//div[@style="text-align: center;"]/p'
                )
                factory_name = address_div.find_elements(By.TAG_NAME, 'span')[0].text
                address = address_div.find_elements(By.TAG_NAME, 'span')[1].text.replace('地址：', '')
            except Exception as e:
                print('地址信息解决出错，link:', link, 'err: ', e)
                factory_name = '工厂名获取出错'
                address = '工厂名获取出错'
            # 获取厂家名称
            print(factory_name, address)

            print('-----------------')
            # 定义商品详情表的数据字典
            data = []
            for span in goods_div:
                name = span.find_element(By.CLASS_NAME, 'offer-attr-item-name').text.strip()
                value = span.find_element(By.CLASS_NAME, 'offer-attr-item-value').text.strip()
                item = {
                    'name': name,
                    'value': value
                }
                data.append(item)
            aliwangwang_button.click()
            try:
                driver.find_element(By.XPATH, '//button[text()="进入网页版"]').click()
                current_handle_index = driver.window_handles.index(driver.current_window_handle)
                driver.switch_to.window(driver.window_handles[current_handle_index + 1])
                driver.find_element(By.XPATH, '//span[@class="next-btn-helper" and text()="使用网页版"]').click()
            except Exception:
                print('没有弹窗选择旺旺版本，默认进入网页版')

            # 点完弹窗，切换回聊天窗口
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if driver.title == '1688旺旺聊天':
                    break
            time.sleep(5)
            print('商品信息获取完毕')
            # 关闭聊天窗口
            driver.close()

            # 关闭商品详情窗口
            driver.switch_to.window(goods_detail_handle)
            driver.close()
            # 切换回原来的窗口
            driver.switch_to.window(original_window)
            # 返回商品详情表的数据字典
            return (str(data), address, factory_name)

        except ValueError as e:
            print("捕获到异常:", e)
            # 手动处理滑动验证
            input('请手动滑动验证码，输入任意字符继续：')
            continue


def get_goods_info(driver, original_window):
    # 获取商品信息的列表
    goods_list = driver.find_element(By.ID, 'sm-offer-list').find_elements(By.CLASS_NAME, 'space-offer-card-box')
    print('-----------------')
    print('开始爬取数据，数据长度为：', len(goods_list))
    for li in goods_list:
        link_div = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.TAG_NAME, 'a')
        link = link_div.get_attribute('href')
        title = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.CLASS_NAME, 'title').text
        price_div = li.find_element(By.CLASS_NAME, 'mojar-element-price')
        price = price_div.find_element(By.CLASS_NAME, 'showPricec').text
        sale_sum = price_div.find_element(By.CLASS_NAME, 'sale').text
        if sale_sum == '':
            sale_sum = '0'
        print('-----------------')
        print(title, price, sale_sum)
        # 插入数据
        with SessionContext() as session:
            # 获取商品详细信息
            detail_data, address, factory_name = get_goods_detail(driver, link, original_window)
            # 插入数据
            goods = GoodsInfo(title=title, price=price, sale_sum=sale_sum, link=link, detail=detail_data,
                              address=address, factory_name=factory_name)
            session.add(goods)
            session.commit()


def check_login_redirect(web_driver):
    max_check_times = 10
    for i in range(max_check_times):
        if web_driver.current_url.startswith(DEFAULT_1688_URL_PREFIX):
            return True
        else:
            time.sleep(2)
    return False


# 启动爬虫程序
def start_crawler(image2url):
    driver = driver_init()
    driver.implicitly_wait(3)

    for imageName, imageUrl in image2url.items():
        print("开始搜索图片：" + imageName)
        crawl_by_image_url(driver, imageName, imageUrl)
    # 关闭浏览器
    driver.quit()


# 根据图片url爬取数据
def crawl_by_image_url(driver, image_name, image_url):
    # 打开链接获取商品信息
    driver.get(DEFAULT_1688_URL_PREFIX)
    if driver.current_url.startswith(LOGIN_URL_PREFIX):
        time.sleep(3)
        if not check_login_redirect(driver):
            print('未检测到登录行为。请关闭浏览器并重启程序后进行登录以继续使用。')
            driver.quit()
            sys.exit()
    # 提供的 cookie 字符串
    cookie_string = '__mwb_logon_id__=dbwdbw1; __waplatid__=dca9c3fa07c24c8cba57a3e62843fd54; ' \
                    'keywordsHistory=%E8%A1%8C%E6%98%9F%E5%8F%91%E5%8A%A8%E6%9C%BA; inquiry_preference=client; ' \
                    'xlly_s=1; lid=dbwdbw1; alicnweb=touch_tb_at%3D1680428191293; ' \
                    'ali_ab=180.109.230.181.1682163543891.3; taklid=70d92190a4ed457c94adc4e871fa9d16; ' \
                    '__cn_logon__=true; __cn_logon_id__=dbwdbw1; last_mid=b2b-2248476908; ' \
                    '_m_h5_tk=e74b569602003528de2a114d150a3c8b_1704553083662; ' \
                    '_m_h5_tk_enc=0c51764d88010bfeecdeb6c383a74a4c; cna=qpnxHcLZDykCATFBUP4VLqTU; ' \
                    'cookie1=AVdHXHZcvIGj9hg1z5Z3ZebSVUEfwSNLF%2BDmf8WRKcc%3D; ' \
                    'cookie2=1f9a6fcae33b94209a7e8b287bbc6db6; cookie17=UUplaXFNqNx8Lg%3D%3D; ' \
                    'sgcookie=E100BlIxDnKnoYqDOQ84qd66VF%2FJGzgSRfQgQLP6S7X%2FZfnagJi%2FqUayEq7xlZF' \
                    '%2FmAkRuzmyGLXAF3NFQ%2FxJZWYWZRx2c9CnnP05dbXmQENMflad33grVIS%2FyTAsB%2FNSzxG6; ' \
                    't=1273e683c073ee8265b69a96880c61d7; _tb_token_=e4933338e3771; sg=187; csg=5f0f1ee6; ' \
                    'unb=2248476908; uc4=nk4=0%40BQOkCq2f08%2BcO6u0Vf%2F0lZRt&id4=0%40U2gvJul3CLHC35j%2FHiGQDlAuSj1Y; ' \
                    'ali_apache_track=c_mid=b2b-2248476908|c_lid=dbwdbw1|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; ' \
                    '_nk_=dbwdbw1; _csrf_token=1704545505759; mwb=tm; ' \
                    'EGG_SESS=1k3SXlytPYtOKy7SJY33yKsHfYgGD8PEVPnGYSHQUIyfdYPyAib8AnAG6iyEKU9YXvJ7ubodSqNfY_c1iN4HKrnSi56b01-t4CAvVf-vkWqNM0DpvAooLkfu5VfzT3r5Y2K-2_1RLNcxIPtSHxS9mngOvZJ9oH1pLxzyQ_oSUEPHnPE_QH7PHfGOE1iioDg63altaTm804ThxR5Q-KKr1BfgPYmNq1LzTXOFesO5kdvGpGzHl6r7-XZBb12kB2hk3TzQBKlH1Pq009N8ISQmk4bNeKbSc6n8Oksb--gkmAXQ4YpMc67OjTfeH6o7AMXKbWxp12RCucoJf58eFqB8bBJv3JmUuS0I-MZb0n9yCFkmsrYQPzikxsCguP_UMur4vOeYPXJzHIKt-RlldUWc3iggPZHPorQvAKGy0WNCMTvvTdYMtbn7Prgz51CNbm2hPqDKGW0rSFCj1yzSPnkJpsl8r8Kd_0sa5MrvunvlyqHm1AYzIRF56y5vId9S66rfMWRMmyU5TGfUj22zAdO4RaFwjwlaNYlkpxAAcJ8WpVaMfg6afyGBN20OHe5aUNbRVzlIj7NDDKw7AZuhOXaTvcS9XuftdHpuYnQaQrS0U_q9II8_Rg5pbTV9bqmDjOZOSeqiyJrzwXHnxFczFU7tx9te5uBfUO4p_KKS47R8BsGm6ZMg3FdL9AaYafB6FU9VTODGc4yIX6McMYSmm3EyLO6hSwlB3HYyblz7oIgZLFI6C7Qx49poFlss4tdHLxXn-gvGS8gte9yemq_r7b3WRnDubnWGvqdquXbPc5BLV5gVmP-AAo-6p2ORhaNK5PuRyvYbAqfiZdjkLEs9CYNLE-MnAql-qtb2nw47tWZS36RUOmxEub1ewVR_VbTy0H7v_7vHfaj-kM1R70d7mjsFqvxbtrQKr9ij12n9JEzu_j9tiGoLFxkIQL7lpRlEnp9qJX_5JKZ8fFk2S5_FmwjxmkAbu7tynM5euK8tcr6I8dsCGlXmgslUn176gBMVZCEknOL2tsNifzL5Uwxep7BETv6b8O3TrtUtZIhFliJKW-ICLO_BvE0GuGxrBb9xCIf1GAWrgB1Zf6OmyEkR-ctBxRSbqYAra4bXNXFU-7Ajj6XxwksrYSAiJh1rubBkZ2nrgNfEf62JveOfYx3ccBnfzWmzWGxmcpw2PojwqNMqoUuaF3AcruC-Yg7trUNosLBbqKd1bpq6AcJ-XhadkOXyEuAIkSJyJ5wMQFl3ze7UOIU1hYb4gOAgl5CUmgcRJPYOkjvnVkcjT3Gu1hIwQts2glj3913wnCbofg3CAr253ni35jEfAu7aC8xRbLVa6v1oT6mZikJDIz3XGolZ0r9nWjZWSSsY2qcieDJurz69ajw3_nkwbtI0YkppIEK-UoHW1u0ZcCf8loQ8lgVu0-2guj0DGHY0thQNfvfHdEzrH2MqxoPzjZ2yPrwMaJYGjRXjQbJwdEgA-3O7pGWFwubyTGgQ7Z17N_vXHelWqD3CvpXAEakDKzEcapcLa6T96N9XfWX9blyNs1PB2nMGD4oC8ZUNosJ_kHXOAxtjNzYN8NgwqrDBK7vGOfPzoA1vVdr5v7xlfqExLNfws4XJV8p4ERElYs3v57IMZnfpse_mg1DZN9nfpfeli4eG-iKYNtHFqghdXfsJYa_ayEfsb0fEC4wlG4XEBhdB6vUfh2_eLstf1Bk7dYt74F61Q1qcedXakAphhdgdFF53KPUrYp8s41S_J1J-Yb7BWA_G0BZ8hPc3363cECnkY-R-T9S8RJW_xd0DrvcqHvh-Kj_egu30sC4hAyGvLtFLd18TSyUNlb80xlJaC88U8tZjopNqfns-; tfstk=ew7eqrAGsyUe4mcfYhYyuopYJJTpEEeXKa9WZ_fkOpv3eWdkz96MqBAorfjNEOKBKeN-445yB0DHqHmijIA--0xoxGlPMO85U_FpZLXlULsQfr1d9ULuh4zbl6UhuIugh5XpwcLJr-wsf4xLuUBq_UFAxkJjN7mMv-XMINq7YtT7TsvZr4lvTHv0kduorNRF_Kf3240l7B-h4DHJsEx1yMko4HA9_KNa_Koyq6CZqGpI20KaXCJbMSn-2HA9_KNa_0nJbZdwhSFA.; l=fBEM5IJRNPMeTcgNBOfwPurza77OSIRAguPzaNbMi9fPO_je5bpfW1B6FlvwC3GVFs3eR3S3hc2kBeYBqIfA2b8E7arqSVDmnmOk-Wf..; isg=BLGxT3U5cNlzJN29fNfuOK0VwD1LniUQHezBYJPGrXiVutEM2-414F_c3E7ccr1I'

    # 将字符串分割成键值对
    cookies = [cookie.split("=") for cookie in cookie_string.split("; ")]

    for cookie in cookies:
        driver.add_cookie({'name': cookie[0], 'value': cookie[1], 'domain': '1688.com'})

    driver.get(image_url)
    # 睡眠3秒，等待浏览器加载完毕
    time.sleep(3)

    # TODO 价格排序后，前面的很可能不是符合图片的，最好还是默认“综合排序”
    # # 按价格排序
    # price_sort_button = driver.find_element(By.XPATH, "//span[@class='sm-widget-txt' and text()='价格']")
    # price_sort_button.click()

    # 循环爬取前20个数据
    for i in range(20):
        print(f'-----------------第{i + 1}页-----------------')
        # 等待浏览器加载完毕
        driver.implicitly_wait(7)
        # 获取当前窗口句柄
        original_window = driver.current_window_handle
        time.sleep(1)
        # 慢慢向下滚动
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        # 再慢慢向上滚动
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        # 滑动鼠标到页面中部
        ActionChains(driver).move_by_offset(0, 300).perform()
        time.sleep(1)

        # 获取商品信息
        get_goods_info(driver, original_window)
    print('-----------------')
    print(image_name + '爬取完毕！')
