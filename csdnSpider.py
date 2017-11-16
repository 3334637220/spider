import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 30)


def run(uid, dir):
    print('login...')
    url = 'http://download.csdn.net/index.php/vip_download/download_client/'
    browser.get(url)
    uname_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
    )
    psw_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#fm1 > input.logging'))
    )
    uname_input.send_keys('qq_22944413')
    psw_input.send_keys('test123')
    submit.click()
    session = requests.Session()
    cookies = browser.get_cookies()

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    print('downloading...')
    response = session.get(url + uid)
    file_name = re.search('filename="(.*?)"', str(response.headers)).group(1)
    dir += '\\' + uid
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = dir + '\\' + file_name
    with open(path, 'wb') as f:
        f.write(response.content)
    print('done.')


if __name__ == '__main__':
    uid = input('输入资源ID: ')
    dir = input('输入下载目录: ')
    run(uid, dir)
