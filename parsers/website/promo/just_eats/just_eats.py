from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from multiprocessing import Pool

from datetime import datetime
from lxml import etree
import pandas as pd
import time

import setting

from database.database import DataBase


class Card_promo():


    def __init__(self, html_card, post_code, city):
        self.html = etree.HTML(html_card)
        self.post_code = post_code
        self.city = city

    def get_head(self):
        try:
            heading = self.html.xpath('//h3')
            return heading[0].text.strip()
        except:
            return 'not found'

    def get_logo_image(self):
        try:
            img_tag = self.html.xpath('//img[@data-test-id="restaurant_logo"]')
            href = img_tag[0].get('src').strip()
            return href
        except:
            return 'not found'


    def get_promo_image(self):
        try:
            img_tag =self.html.xpath('//*[@data-test-id="restaurant-cuisine-image"]')
            href = img_tag[0].get('style').strip()[23:-3]
            return href
        except:
            return 'not found'

    def get_category_foods(self):
        try:
            tag = self.html.xpath('//*[@data-test-id="restaurant-cuisines"]/li')
            return ", ".join([i.text for i in tag])
        except:
            return 'not found'
    def get_stamp_card(self):
        try:
            tag = self.html.xpath('//div[@data-test-id="restaurant-stampcard-tag"]//p')
            return tag[0].text.strip()
        except:
            return 'not found'

    def get_discounts(self):
        try:
            tag = self.html.xpath('//*[@data-test-id="restaurant-discounts"]/span[2]')
            print(f"disc{tag}")
            return tag[0].text.strip()
        except:
            return 'not found'

    # лучше доп функция
    def get_delivery_order(self):
        try:
            try:
                tag_delivery = self.html.xpath('//div[@data-test-id="restaurant-delivery-fees"]/p/span[2]')
            except:
                tag_delivery = ['Not found']
            try:
                tag_min_order = self.html.xpath('//p[@data-test-id="restaurant-fees-min-order"]/span')
            except:
                tag_min_order = ['Not found']
            return [tag_delivery[0].text, tag_min_order[0].text]
        except:
            return ["not found", "not found"]


    def get_time(self):
        try:
            tag = self.html.xpath('//*[@data-test-id="restaurant-eta"]/span[2]')
            return tag[0].text.strip()
        except:
            return 'not found'

    def get_distance(self):
        try:
            tag = self.html.xpath('//*[@data-test-id="restaurant-location"]/span[2]')
            return tag[0].text
        except:
            return 'not found'

    def get_pre_order(self):
        try:
            try:
                tag_type = self.html.xpath('//*[@data-test-id="restaurant-availability-type"]/span[2]')
            except:
                tag_type = ['Not found']
            try:
                tag_opening = self.html.xpath('//*[@data-test-id="restaurant-availability-message"]')
            except:
                tag_opening = ['Not found']

            return [tag_type[0].text, tag_opening[0].text]
        except:
            return ["not found", "not found"]

    def get_rating(self):
        try:
            tag = self.html.xpath('//span[@data-test-id="restaurant-rating"]')
            return tag[0].text.strip()
        except:
            return 'not found'

    def get_voice_rating_count(self):
        try:
            tag = self.html.xpath('//strong[@data-test-id="rating"]')
            return tag[0].text.strip()
        except:
            return 'not found'


    def get_not_taking_orders_at_the_moment(self):
        try:
            tag = self.html.xpath('//div[@data-test-id="restaurant-offline"]//p')
            return tag[0].text.strip()
        except:
            return 'not found'

    def get_info(self):
        head = self.get_head()
        logo_image = self.get_logo_image()
        promo_image = self.get_promo_image()
        category_foods = self.get_category_foods()
        stamp_card = self.get_stamp_card()
        discounts = self.get_discounts()
        delivery_order = self.get_delivery_order()
        time = self.get_time()
        distance = self.get_distance()
        pre_order = self.get_pre_order()
        rating = self.get_rating()
        rating_count = self.get_voice_rating_count()
        not_taking_orders_at_the_moment = self.get_not_taking_orders_at_the_moment()


        date = datetime.now().strftime("%d.%m.%Y")
        post_code = self.post_code

        print(date)
        print(f'head: {head}')
        print(f'logo_image: {logo_image}')
        print(f'promo_image: {promo_image}')
        print(f'category_foods: {category_foods}')
        print(f'stamp_card: {stamp_card}')
        print(f'discounts: {discounts}')
        print(f'delivery_order: {delivery_order}')
        print(f'time: {time}')
        print(f'distance: {distance}')
        print(f'pre_order: {pre_order}')
        print(f'rating: {rating}')
        print(f'rating_count: {rating_count}')
        print(f'not_taking_orders_at_the_moment: {not_taking_orders_at_the_moment}')


        return {
            'date': date,
            'post_code': post_code,
            'city': self.city,
            'head': head,
            'logo_image': logo_image,
            'promo_image': promo_image,
            'category_foods': category_foods,
            'stamp_card': stamp_card,
            'discounts': discounts,
            'delivery_order_from': delivery_order[0],
            'delivery_order_min': delivery_order[1],
            'time': time,
            'distance': distance,
            'pre_order_0': pre_order[0],
            'pre_order_1': pre_order[1],
            'rating': rating,
            'rating_count': rating_count,
            'not_taking_orders_at_the_moment': not_taking_orders_at_the_moment,
        }





def get_card_deals_html(driver):
    return [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//*[@data-test-id="restaurant"]')]


def get_count_restaurants(driver):
    return driver.find_element(By.XPATH, '//div[@data-test-id="refine-sidebar"]//label[span[contains(text(), "Special")]]//span[@data-test-id="filter-pill-number"]').text.strip()


def scroll_page(driver):
    timer_scrolling = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        timer_scrolling +=1
        current_value_cards = len(get_card_deals_html(driver))
        count_card = int(get_count_restaurants(driver))
        print(count_card)
        print(f'current: {current_value_cards}')
        if current_value_cards == count_card:
            print('While normal work')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            break
        elif timer_scrolling == 10:
            print('While end time')
            # запасной вариант выхода с цикла
            break

def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[@data-test-id="accept-all-cookies-button"]').click()
        time.sleep(3)
    except:
        pass

def set_post_code(post_code, driver):
    driver.find_element(By.XPATH, '//input[@name="postcode"]').send_keys(f'{post_code}')
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@name="postcode"]').send_keys(Keys.ENTER)
    time.sleep(8)

def run_browser():
    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])

    url = 'https://www.just-eat.co.uk/offers'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver
def parse(arg):
    post_code = arg[0]
    city = arg[1]
    driver = run_browser()

    click_accept(driver)

    set_post_code(post_code, driver)

    scroll_page(driver)

    card_deals_html = get_card_deals_html(driver)

    driver.close()
    driver.quit()
    
    data = [Card_promo(i, post_code, city).get_info() for i in card_deals_html]

    data = [pd.DataFrame([i]) for i in data]

    data_frame = pd.concat(data)
    # date = datetime.now().strftime("%d.%m.%Y")
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_JUST_EATS_PROMO')


def start_just_eats_promo():
    post_codes = [
        'W1C 1LX',
        'CF10 1PN',
        'BT1 5AA',
        'G1 3SQ',
        'B2 4QA',
        'L1 8JQ',
        'LS1 1UR',
        'M2 5DB'
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

    with Pool(processes=5) as p:
        p.map(parse, zip(post_codes,city))


