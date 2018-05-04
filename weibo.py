from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# chrome_options = Options()
# #chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#
# prefs = {
#     'profile.default_content_setting_values': {
#         'images': 2,
#         'javascript': 1,
#         'notifications': 2
#     }
# }
# chrome_options.add_experimental_option('prefs', prefs)
# browser = webdriver.Chrome(chrome_options=chrome_options)

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

print('初始化...')
wait = WebDriverWait(browser, 30)

def login(username, password):
    print('正在登录...')
    browser.maximize_window()
    browser.get('https://service.account.weibo.com/index?type=5&status=0&page=1')


    loginname = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#loginname'))
    )
    loginpwd = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input'))
    )

    time.sleep(2)
    loginname.send_keys(username)
    loginpwd.send_keys(password)
    submit = 'document.getElementsByClassName("W_btn_a btn_32px")[0].click();'
    browser.execute_script(submit)
    wait.until(
        EC.presence_of_element_located(
            (By.ID, 'pl_service_showcomplaint')
        )
    )
    print('登录成功!')


def spider(startIndex, endIndex):
    pattern = re.compile(r".*m_table_tit\"><a href=\"(.*?)\"")
    pattern2 = re.compile(r".*<input type=\"hidden\" node-type=\"right_top\" value=\"([\s\S]*?)>")
    for i in range(startIndex, endIndex+1):
        browser.get('https://service.account.weibo.com/index?type=5&status=0&page=' + str(i))
        html = browser.page_source
        rs = re.findall(pattern, html)
        print('第'+str(i)+'页')
        for r in rs:
            browser.get('https://service.account.weibo.com'+r)
            doc = pq(browser.page_source)
            m_title = doc('.top_title .m_title').text()
            name = doc('p.mb.W_f14').text().split(" ")
            address1 = doc('div.W_main_half_l > div > div:nth-child(3) > div > p:nth-child(3)').text()
            address2 = doc('div.W_main_half_r > div > div.user.bg_orange2.clearfix > p:nth-child(3)').text()
            qianming1 = doc('div.W_main_half_l > div > div:nth-child(3) > div > p:nth-child(4)').text()
            qianming2 = doc('div.W_main_half_r > div > div.user.bg_orange2.clearfix > p:nth-child(4)').text()
            time = doc(' div.W_main_half_r > div > div > div > div > p').text()[11:-5]
            content = doc('div.W_main_half_r > div > div > div > div > div').text()

            if '查看全文' in content:
                content = re.findall(pattern2, browser.page_source)[0]

            print('标题:'+m_title)
            print('举报人名:'+name[0])
            print('举报人地址:'+address1)
            print('举报人签名:'+qianming1)
            print('被举报人名:'+name[1])
            print('被举报人地址:'+address2)
            print('被举报人签名:'+qianming2)
            print('被举报微博发布时间:'+time)
            print('被举报微博内容:'+content)
            print('-'*50)


if __name__ == '__main__':
    login('18652030106', 'jiguantong')
    spider(1,1)

