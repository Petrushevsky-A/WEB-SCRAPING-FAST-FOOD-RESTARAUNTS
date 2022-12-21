from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import datetime
import pandas as pd
import time

import setting
from database.database import DataBase


class SupermarcsPromoParser():

    def __init__(self):
        self.url = r'https://order.supermacs.ie/click-collect'
        self.row_search = 'dublin'
        self.source = r'https://order.supermacs.ie'
        self.current_brand = ''
        self.current_category = ''

        self.driver = None
        self.enter()
        self.open_url()
        self.search()
        self.start_parse()



        time.sleep(3333)

        self.exit()
    def enter(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        # print(1)
        # return self

    def open_url(self, url=None):
        if url:
            self.driver.get(url=url)
        else:
            self.driver.get(url=self.url)
        time.sleep(3)

    def exit(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()


    def search(self):
        # $x('//input[contains(@id, "store-name")]')
        input_search = self.driver.find_element(By.XPATH, r'//input[contains(@id, "store-name")]')
        input_search.send_keys(self.row_search)
        time.sleep(2)
        # input_search.send_keys(Keys.ENTER)
        # $x('(//*[@class="store-search-result-item"]//*[contains(text(), "Click")])[1]')

        xpath = r'(//*[@class="store-search-result-item"]//span[contains(text(), "Click")])[1]'
        place = self.driver.find_element(By.XPATH, xpath)
        place.click()
        time.sleep(3)

    def start_parse(self):
        brands = self.get_brands()
        # print(len(brands))
        # print(type(brands))
        # print(brands)
        # x = lambda x: print(x.text)
        # print([x(i) for i in brands])
        for brand in brands:
            # print(id(brand))
            # print(brand)
            # print(len(brand))
            # print(len(brands))
            # print(brand is brands)
            # time.sleep(3333)

            # current_brand = brand.text
            # current_brand = brand.find_element(By.XPATH, r'.//h3').get_attribute('textContent')
            current_brand = brand.find_element(By.XPATH, r'.//h3').text
            print(current_brand)
            # current_brand = brand.find_element(By.XPATH, fr'//div[@class="category-parent-menu"]/div[{index}]//h3').get_attribute('textContent')


            url_brand = brand.find_element(By.XPATH, r'.//a').get_attribute('href')
            print(url_brand)

            self.open_url(url_brand)
        #     # brand.click()
        #     time.sleep(1)
        #     categories = self.get_category()
        #     for category in categories:
        #         current_category = category.text
        #         items = self.get_items()
        #         for item in items:
        #             date = datetime.now().strftime("%d.%m.%Y")
        #
        #             price = self.get_price()
        #             title = 123
        #             image_url = self.get_image()
        #             html_cards = 123
        #
        #
        #             print(f'price {price}')
        #             print(f'title {title}')
        #             print(f'image_url {image_url}')
        #             print(f'html_cards {html_cards}')
        #             # data = {
        #             #     'start_date': date,
        #             #     'end_date': date,
        #             #     'brand': current_brand,
        #             #     'address': 1,
        #             #     'city': 1,
        #             #     'post_code': 1,
        #             #     'segment': 1,
        #             #     'category': current_category,
        #             #     'category_2': '',
        #             #     'category_3': '',
        #             #     'category_4': '',
        #             #     'item': 1,
        #             #     'source': 1,
        #             #     'region': 1,
        #             #     'price': 1,
        #             #     'status': 'on',
        #             #     'picture': 1,
        #             #     'html_cards': 1,
        #             #     'post_code_address': 1,
        #             #     'description': '',
        #             # }
        #             #
        #             # data_frame = pd.DataFrame(data)
        #             # self.to_stg_db()
        #
        # return True

    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)
    def get_element_items(self):
        pass

    def get_items(self):
        return self.driver.find_elements(By.XPATH, r'//div[@class="product-list"]')






    def get_image(self):
        pass

    def get_price(self):
        pass
    def get_title(self):
        pass
    def get_html_cards(self):
        pass

    def get_description(self):
        pass








    def get_brands(self):
        # $x('//div[@class="category-parent-menu"]/*')
        for brand in  self.driver.find_elements(By.XPATH, r'//div[@class="category-parent-menu"]/div'):
            yield brand

    def get_address(self):
        pass

    def get_category(self):
        # $x('//ul[@class="menu sub-nav"]/li')
        try:
            return self.driver.find_elements(By.XPATH, r'//ul[@class="menu sub-nav"]/li')
        except:
            return ['', ]


