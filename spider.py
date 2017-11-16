import re
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 30)

browser.set_window_size(1400, 900)


def search(key):
    try:
        print('init...')
        browser.get('https://www.aliexpress.com')
        browser.refresh()
        print('search for 1st page...', end='\t')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#search-key'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#form-searchbar > div.searchbar-operate-box > input'))
        )
        input.send_keys(key)
        submit.click()
        print('done')
        return get_products()
    except TimeoutError:
        return search(key)


def next_page(page_number):
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#pagination-bottom-input'))
    )
    submit = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#pagination-bottom-goto'))
    )
    input.clear()
    input.send_keys(page_number)
    submit.click()
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#pagination-bottom > div.ui-pagination-navi.util-left > span.ui-pagination-active'),
            str(page_number))
    )
    return get_products()


def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#hs-below-list-items .list-item'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#hs-below-list-items .list-item .item').items()
    products = []
    for item in items:
        title = item.find('.product').attr('title')
        price = item.find('.price-m .value').text()
        price = price.replace('US $', '', 1)
        star = item.find('.star-s').attr('title')
        if star:
            star_rating = star[13:16]
        else:
            star_rating = None
        orders = item.find('.order-num-a').text()
        if orders:
            orders_num = re.compile('(\d+)').search(orders).group(1)
        feedback = item.find('.rate-num').attr('title')
        if feedback:
            feedback_num = re.compile('(\d+)').search(feedback).group(1)
        else:
            feedback_num = None
        seller = item.find('.util-clearfix').text()
        seller_rating = item.find('.score-icon-new').attr('sellerpositivefeedbackpercentage')
        if seller_rating:
            seller_rating = seller_rating + '%'

        product = {
            'title': title,
            'price': price,
            'star_rating': star_rating,
            'orders_num': orders_num,
            'feedback_num': feedback_num,
            'seller': seller,
            'seller_rating': seller_rating
        }
        products.append(product)

    return products


def save(products, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'price', 'star_rating', 'orders_num',
                         'feedback_num', 'seller', 'seller_rating'])
        for p in products:
            info = []
            for k in p:
                info.append(p[k])
            writer.writerow(info)


def main():
    key = input('input the key: ')
    page_num = 10
    products = []
    products += search(key)
    for i in range(2, page_num + 1):
        print('search for ' + str(i) + 'st page...', end='\t')
        products += next_page(i)
        print('done')
    print('save data...', end='\t')
    save(products, key + '.csv')
    print('done')


if __name__ == '__main__':
    main()
