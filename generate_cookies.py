from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
import time


# 记录手机号和已添加进入白名单的验证码
mobile = 17820722788
verification_code = 1234
account = 'test@xiaopeng.com'
password = 123456
url = 'http://pmall.test.xiaopeng.local/order/list-v2'
adm_url = 'http://e.test.xiaopeng.local/#/login?forward_url=http%3A%2F%2Fmall-admin.test.xiaopeng.local%2F#/order/list'


class GenerateCookies(object):

    # 获取C端cookies函数
    def generate_cookies(self):

        # 无头浏览模式
        '''

        option = ChromeOptions()
        option.add_argument("--headless")
        driver = webdriver.Chrome(options=option)
        '''

        # 打开指定url
        driver = webdriver.Chrome()
        driver.get(url)

        # 显示等待：先让页面元素加载完再进行赋值登录，否则会出现定位元素失败的情况；如果try中异常则抛“登陆失败”并退出
        # 隐式等待要规定时间，不够灵活
        try:
            mobile_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'mobile-input'))
            )
            mobile_input.send_keys(mobile)
            sms_code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'sms-code-input'))
            )
            sms_code_input.send_keys(verification_code)
            # 同意登陆协议
            agree_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'agree-policy-input'))
            )
            agree_input.click()

            # 点击登录
            driver.find_element(By.ID, 'login-submit-btn').click()
            # 一定要等待一段时间，否则cookie不全
            time.sleep(5)
            driver.refresh()



        except 'ERROR':
            driver.quit()
            print("登陆失败")

        # get_cookie()获取的是字典类型，单个的键值对
        # get_cookies()获取的是由字典组成列表的cookies，是一个完整的cookie
        cookies_list = driver.get_cookies()

        print("cookie_list:", cookies_list)

        # 将列表形的cookies重新拼接为需要的格式
        cookies = []
        for cookie in cookies_list:
            cookies.append(cookie['name'] + '=' + cookie['value'])

        # 把零散的cookies按;分隔符，组装成字符串，传入requestheader
        cookies = ";".join(cookies)
        print("cookies:", cookies)

        return cookies

    # 将获取到的C端cookie写入储存到指定文件里，内容刷新会覆盖
    def write_in(self, cookies):
        with open('cookie_init.txt', 'w', encoding='utf-8') as f:
            f.write(str(cookies))


    def adm_generate_cookies(self):
        '''
        # 无头浏览模式
        option = ChromeOptions()
        option.add_argument("--headless")
        driver = webdriver.Chrome(options=option)
        '''
        # 打开指定url
        driver = webdriver.Chrome()
        driver.get(adm_url)

        try:
            account_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入账号']"))
            )
            account_input.send_keys(account)
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入密码']"))
            )
            password_input.send_keys(password)

            # 点击登录
            driver.find_element(By.CLASS_NAME, 'login-btn').click()
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'el-button--medium').click()
            time.sleep(1)
            # 刷新后再次输入账号密码进入
            account_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入账号']"))
            )
            account_input.send_keys(account)
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入密码']"))
            )
            password_input.send_keys(password)
            # 点击登录
            driver.find_element(By.CLASS_NAME, 'login-btn').click()
            time.sleep(5)
            driver.refresh()



        except 'ERROR':
            driver.quit()
            print("登陆失败")

        # get_cookie()获取的是字典类型，单个的键值对
        # get_cookies()获取的是由字典组成列表的cookies，是一个完整的cookie
        adm_cookies_list = driver.get_cookies()

        print("adm_cookie_list:", adm_cookies_list)

        # 将列表形的cookies重新拼接为需要的格式
        adm_cookies = []
        for cookie in adm_cookies_list:
            # 防止value为空的时候后传入获取的cookie报错
            if cookie['value'] != '':
                adm_cookies.append(cookie['name'] + '=' + cookie['value'])


        # 把零散的cookies按;分隔符，组装成字符串，传入requestheader
        adm_cookies = ";".join(adm_cookies)
        print("adm_cookies:", adm_cookies)

        return adm_cookies

    # 将获取到的B端cookie写入储存到指定文件里，内容刷新会覆盖
    def adm_write_in(self, adm_cookies):
        with open('adm_cookie_init.txt', 'w', encoding='utf-8') as f:
            f.write(str(adm_cookies))


if __name__ == '__main__':
    gen = GenerateCookies()
    cookies = gen.generate_cookies()
    adm_cookies = gen.adm_generate_cookies()
    gen.write_in(cookies)
    print('C端cookies已更新')
    gen.adm_write_in(adm_cookies)
    print('B端cookies已更新')





