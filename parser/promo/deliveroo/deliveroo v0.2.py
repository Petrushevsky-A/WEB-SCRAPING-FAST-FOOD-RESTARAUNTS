import time
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd

import numpy as np

from multiprocessing import Pool
from lxml import etree

class Card_promo():

    def __init__(self, html_card, post_code,city, current_offer_filter):
        self.html = etree.HTML(html_card)
        self.post_code = post_code
        self.current_offer_filter = current_offer_filter
        self.city = city

    def get_promotion(self):
        try:
            text = [i.text for i in self.html.xpath('//div[contains(@class, "PromotionTagOverlay")]//span[contains(@class,  "HomeFeedUILines")]/span')]
            return ", ".join(text)
        except:
            pass

    def get_image_background(self):
        try:
            url_image = [i.get('style') for i in self.html.xpath('//div[contains(@style, "background-image: url")]')]
            return url_image[0][23:-3]
        except:
            pass

    def get_time(self):
        try:
            text = [i.text for i in self.html.xpath('//ul[contains(@class, "Bubble")]/li/span/span')]
            return ": ".join(text)
        except:
            pass

    def get_name(self):
        try:
            text = [i.text for i in self.html.xpath('//ul/li//p')]
            return text[0]
        except:
            pass

    def get_rating(self):
        try:
            text = [i.text for i in self.html.xpath(
                '//ul[contains(@class, "Bubble") != "Bubble"]/li[2][contains(@class, "HomeFeedUILines")]/span[3]/span')]
            return text[0]
        except:
            pass

    # def get_delivery_cost(self):
    #     try:
    #         text = [i.text for i in self.html.xpath(
    #             '//div[contains(@class, "PromotionTagOverlay")]//span[contains(@class,  "HomeFeedUILines")]/span')]
    #         return text
    #     except:
    #         pass

    def get_categorys_food(self):
        try:
            text = [i.text for i in self.html.xpath(
                '//ul[contains(@class, "Bubble") != "Bubble"]/li[2][contains(@class, "HomeFeedUILines")]/span/span')]
            return ", ".join(text[4::2])
        except:
            pass

    def get_distanace(self):
        try:
            text = [i.text for i in self.html.xpath(
                '//ul[contains(@class, "Bubble") != "Bubble"]/li[3][contains(@class, "HomeFeedUILines")]/span/span')]
            return text[0]
        except:
            pass

    def get_delivery(self):
        try:
            text = [i.text for i in self.html.xpath(
                '//ul[contains(@class, "Bubble") != "Bubble"]/li[3][contains(@class, "HomeFeedUILines")]/span/span')]
            return text[2]
        except:
            pass

    def get_status(self):
        try:
            text = [i.text for i in self.html.xpath(
                '//span[contains(text(), "Open") or contains(text(), "Closed")]')]
            return text[0]
        except:
            pass




    def get_info(self):
        promotion = self.get_promotion()
        image_background = self.get_image_background()
        time = self.get_time()




        date = datetime.now().strftime("%d.%m.%Y")
        post_code = self.post_code
        current_offer_filter = self.current_offer_filter
        name =self.get_name()
        rating =self.get_rating()
        # delivery_cost=self.get_delivery_cost()

        categorys_food =self.get_categorys_food()
        distanace =self.get_distanace()
        delivery = self.get_delivery()



        status = self.get_status()
        print(date)
        print(f'name {name}')
        print(f'promotion {promotion}')
        print(f'image_background {image_background}')

        print(f'time {time}')
        print(f'rating {rating}')

        print(f'categorys_food {categorys_food}')
        print(f'distanace {distanace}')
        print(f'delivery {delivery}')
        print(f'status {status}')
        print('==============')

        return {
            'date': date,
            'post_code': post_code,
            'city':self.city,
            'current_offer_filter': current_offer_filter,
            'name': name,
            'promotion': promotion,
            'image_background': image_background,
            'time': time,
            'rating': rating,
            'categorys_food': categorys_food,
            'distanace': distanace,
            'delivery': delivery,
            'status': status,
        }









def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(1)
    except:
        pass


def set_post_code(post_code, driver):
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(f'{post_code}')
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(Keys.ENTER)
    time.sleep(8)


def run_browser():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    url = 'https://deliveroo.co.uk/'
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver

def get_offers_filter(driver):
    tag_li_filter = driver.find_elements(By.XPATH, '//ul[contains(@class, "FilterList")]/li')[1:]
    print('get_offers_filter')
    return tag_li_filter

def click_category(driver, category):
    category.click()
    time.sleep(2)
    print('click_category')
    return

def get_card_deals_html(driver):
    html_card = [i.get_attribute("innerHTML") for i in driver.find_elements(By.XPATH, "//ul[contains(@class, 'HomeFeedGrid')]/li")]
    print(f"count cards: {len(html_card)}")
    return html_card

def get_current_offer_filter(driver):
    text_offer = "ERROR"
    try:
        text_offer = driver.find_element(By.XPATH, '//div[contains(@class, "HomeSummary")]//div/p[1]').text
        print('try name offer')
    except:
        tag_li_list_is_selected = [i.is_selected() for i in driver.find_elements(By.XPATH, '//ul[contains(@class, "FilterList")]/li//input')]
        select_index_tag_li = tag_li_list_is_selected.index(True)
        text_offer = driver.find_element(By.XPATH, '//ul[contains(@class, "FilterList")]/li/label/span[1]')
        print('except name offer')
    return text_offer

def ok_click_popup(driver):
    try:
        driver.find_element(By.XPATH, '//button/span[text() = "OK"]').click()
        time.sleep(2)
        print('ok_click_popup')
    except:
        pass

def scroll_page(driver):
    timer_scrolling = 0
    time.sleep(2)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element(By.XPATH, '//div[@id="home-feed-container"]').click()
    # for i in range(10):
    # driver.execute_script("window.scrollTo({top: document.documentElement.scrollHeight, left: 0, behavior: 'smooth'})")
    # stop_scrolling_element = driver.find_element(By.XPATH, '//div[@id="page-footer"]')
    # while True:
    #     time.sleep(1)
    #     driver.find_element(By.XPATH, '//html').send_keys(Keys.PAGE_DOWN)
    #     if driver.execute_script("arguments[0].scrollIntoView();", stop_scrolling_element):
    #         break

    for to_scrolling_element in driver.find_elements(By.XPATH, '//ul/li[contains(@class, "HomeFeedGrid")]'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(.1)
    time.sleep(2)



def parse(arg):

    post_code = arg[0]
    city = arg[1]
    print(post_code)
    driver = run_browser()

    click_accept(driver)

    set_post_code(post_code, driver)

    ok_click_popup(driver)

    offers = get_offers_filter(driver)

    data_all_offers = []
    for offer in offers:
        try:
            click_category(driver, offer)
            scroll_page(driver)
            card_deals_html = get_card_deals_html(driver)
            current_offer_filter = get_current_offer_filter(driver)
            data_all_offers.append([Card_promo(i, post_code,city, current_offer_filter).get_info() for i in card_deals_html])
        except:
            continue

    driver.close()
    driver.quit()

    data_all_offers = sum(data_all_offers, [])

    data = [pd.DataFrame([i]) for i in data_all_offers]
    date = datetime.now().strftime("%d.%m.%Y")
    data = pd.concat(data)
    pd.DataFrame(data).to_excel(f'deliveroo_{post_code}_{date}.xlsx')


    columns = {
        0: 'dates',
        1: 'post_codes',
        2: 'city',
        3: 'head',
        4: 'names',
        5: 'descriptions',
        6: 'link_images',
        7: 'foods_category',
        8: 'delivery',
        9: 'times',
    }
    # data = [Card_promo(i, post_code, category).get_info() for i in card_deals_html]
    #
    # data = [pd.DataFrame([i]) for i in data]
    #
    # data = pd.concat(data)
    # pd.DataFrame(data).to_excel(f'just_eats_{post_code}.xlsx')


if __name__ == '__main__':
    post_codes = [
        'W1C 1LX',
        'CF10 1PN',
        'BT1 5AA',
        'G1 3SQ',
        'B2 4QA',
        'L1 8JQ',
        'LS1 1UR',
        'M2 5DB',
    ]

    city = [
        'London',
        'Cardiff',
        'Belfast',
        'Glasgow',
        'Birmingham',
        'Liverpool',
        'Leeds',
        'Manchester'
    ]

    with Pool(processes=10) as p:
        temp = list(zip(post_codes, city))[:]
        p.map(parse, temp)


