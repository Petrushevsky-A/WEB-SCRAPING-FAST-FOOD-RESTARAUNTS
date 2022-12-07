import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.select import Select

import setting
from datetime import datetime
from itertools import repeat


class DominosParser():

    def __init__(self, post_code):
        self.post_code = post_code
        self.url = 'https://www.dominos.co.uk/'
        self.driver = None
        self.data_products = []
        self.data_parsed = []
        self.date = repeat(datetime.now().strftime("%d.%m.%Y"))
        self.brand = repeat('Dominos')
        self.region = repeat('UK')
        self.status = repeat('on')
        self.source = repeat('https://www.dominos.co.uk/')
        self.collumn = [
                        'Start date',
                        'End date',
                        'Brand',
                        'Address',
                        'City',
                        'Postcode',
                        'Segment',
                        'Category',
                        'Category 2',
                        'Category 3',
                        'Category 4',
                        'Item',
                        'Source',
                        'Region',
                        'Price(£)',
                        'Status',
                        'Picture',
                    ]

    def __enter__(self):
        self.driver = self.run_browser()
        time.sleep(2)
        self.open_url(self.url)
        time.sleep(3)

        self.accept_click()
        time.sleep(1)
        self.input_post_code()
        time.sleep(2)
        self.click_first_button_list()
        self.close_popup()
        time.sleep(2)
        self.scrolling_page()
        self.address = self.get_address()
        self.address_repeat = repeat(self.address)
        null = repeat('')
        self.data_products = list(zip(self.date, self.date, self.brand, self.address_repeat, null, repeat(self.post_code), null, self.data_parsed, self.source, self.status, self.region))
        print(self.data_parsed)

        print(self.data_products)

        pd.DataFrame(self.data_parsed).to_excel(f'dominos_1{self.post_code}_{self.date}.xlsx')
        pd.DataFrame(self.data_products).to_excel(f'dominos{self.post_code}_{self.date}.xlsx')


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    #     self.driver.close()
    #     self.driver.quit()
    #     return True

    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        return driver

    def open_url(self, url):
        self.driver.get(url=url)
        time.sleep(5)

    def accept_click(self):

        try:
            self.driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
            time.sleep(2)
        except:
            print("Not found accept")

    def input_post_code(self):
        # $x('//input[@type="text"]')
        self.driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(self.post_code)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(Keys.ENTER)
        time.sleep(7)

    def click_first_button_list(self):
        # $x('//*[contains(text(), "Collect")]/ancestor::button')
        try:
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Collect")]/ancestor::button').click()
            time.sleep(4)
        except:
            print("not found button collect")

    def close_popup(self):
        # $x('//button[contains(@class, "close")]')
        try:
            self.driver.find_element(By.XPATH, '//button[contains(@class, "close")]').click()
            time.sleep(2)
        except:
            print("not found button collect")

    def scrolling_page(self):

        # все карточки товаров
        #     $x('//*[@data-ref-id="base-menu-item-container"]')
        # $x('(//*[@data-ref-id="base-menu-item-container"])[66]/ancestor::section[@class="base-scroll-section"]').map(i => i.getAttribute("id"))
        section_products = self.driver.find_elements(By.XPATH,
                                                         '//section[@class="base-scroll-section"]')


        for section_product in section_products:
            card_products = section_product.find_elements(By.XPATH,
                                                      './/*[@data-ref-id="base-menu-item-container"]')
            category_products = section_product.get_attribute('id')

            # print(card_products)
            for card_product in card_products:
                time.sleep(0.3)
                # print(category_products)
                # print(card_product.get_attribute('outerHTML'))
                # $x('//div[contains(@class, "variants-container")]//select[@data-ref-id="base-select-input"]/option[not(@disabled="disabled")]').map(i => i.text)
                head = card_product.find_element(By.XPATH, './/h3').text
                print(head)

                try:
                    calories = card_product.find_element(By.XPATH, './/span[contains(@data-ref-id, "product-calories")]').get_attribute('innerHTML')
                    print(f'calories {calories}')
                except:
                    calories = ''
                    print(f'calories {calories}')

                try:
                    image = card_product.find_element(By.XPATH, './/img').get_attribute('src')
                    print(f'image {image}')
                except:
                    image = ''
                    print(f'image {image}')

                try:
                    price = card_product.find_element(By.XPATH, './/span[@data-ref="base-menu-price-text"]').get_attribute('innerHTML').strip()
                    print(f'image {price}')
                except:
                    price = ''
                    print(f'image {price}')

                try:

                    select_size_options = card_product.find_elements(By.XPATH,
                                                          './/div[contains(@class, "variants-container")]//select[@data-ref-id="base-select-input"]/option[not(@disabled="disabled")]')
                    select_size = Select(card_product.find_element(By.XPATH,
                                                          './/div[contains(@class, "variants-container")]//select[@data-ref-id="base-select-input"]'))
                    # print(select_size_options)
                    print(len(select_size_options))

                    for option in select_size_options:
                        time.sleep(1)

                        try:
                            image = card_product.find_element(By.XPATH, './/img').get_attribute('src')
                            print(f'image {image}')
                        except:
                            image = ''
                            print(f'image {image}')

                        try:
                            price = card_product.find_element(By.XPATH,
                                                              './/span[@data-ref="base-menu-price-text"]').get_attribute(
                                'innerHTML').strip()
                            print(f'image {price}')
                        except:
                            price = ''
                            print(f'image {price}')

                        try:
                            calories = card_product.find_element(By.XPATH,
                                                                 './/span[contains(@data-ref-id, "product-calories")]').get_attribute(
                                'innerHTML').strip()
                            print(f'calories {calories}')
                        except:
                            calories = ''
                            print(f'calories {calories}')

                        current_size = option.text
                        select_size.select_by_visible_text(option.text)
                        time.sleep(1)

                        self.data_parsed.append([
                                                    category_products,
                                                    head,
                                                    calories,
                                                    image,
                                                    price,
                                                    current_size,
                                                ])

                        self.driver.execute_script("arguments[0].scrollIntoView();", card_product)
                        time.sleep(0.2)
                        continue
                except:
                    # time.sleep(3333)

                    # choose(всплывающее меню)
                    try:
                        print('choooooooooOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOse')
                        self.driver.find_element(By.XPATH, r'//button[contains(@data-ref-id, "base-menu-card")]').click()
                        time.sleep(2)
                        # $x('//section[contains(@class, "base-cards-tray")]//section/div')
                        tray_cards = self.driver.find_element(By.XPATH, '//section[contains(@class, "base-cards-tray")]//section/div')
                        for tray_card in tray_cards:
                            head = tray_card.find_element(By.XPATH, './/h3').text
                            print(f'head chose {head}')
                            calories = tray_card.find_element(By.XPATH, './/*[contains(@data-ref-id, "product-calories")]').text
                            print(calories)
                            price = tray_card.find_element(By.XPATH, './/span[@data-ref="base-menu-price-text"]')
                            print(price)

                            self.data_parsed.extend([
                                                        category_products,
                                                        head,
                                                        calories,
                                                        image,
                                                        price,
                                                        'Not found',
                                                    ])
                            self.driver.execute_script("arguments[0].scrollIntoView();", card_product)
                            time.sleep(0.2)
                            continue

                        # $x('//section[contains(@class, "base-cards-tray")]//section/div//span[@data-ref="base-menu-price-text"]')
                        # $x('//button[contains(@data-ref-id, "base-menu-card")]')
                        # $x('//section[contains(@class, "base-cards-tray")]')
                    except Exception as ex:
                        print('Choose error')


                self.data_parsed.append([
                                            category_products,
                                            head,
                                            calories,
                                            image,
                                            price,
                                            'Not found',
                                        ])


                self.driver.execute_script("arguments[0].scrollIntoView();", card_product)
                time.sleep(0.2)


    def get_address(self):
        # $x('//span[@class="nav-store-name"]/ancestor::li')
        try:
            # self.driver.find_element(By.XPATH,
            #                     r'(//*[contains(text(), "Collection")]/ancestor::div/a)[1]').click()
            # $x('(//*[contains(text(), "Collection")]/ancestor::div[a])[1]')
            # $x('//*[contains(text(), "Collection")]/ancestor::div[contains(@class, "button-container")]')
            url_address_info = self.driver.find_element(By.XPATH,
                                r'(//*[contains(text(), "Collection")]/ancestor::div/a)[1]').get_attribute('href')
            self.open_url(url_address_info)
            time.sleep(2)

        except Exception as ex:
            print(ex)
            address = ''
        try:
            # $x('//*[contains(@data-ref-id, "address")]')
            address = ", ".join([i.text for i in self.driver.find_elements(By.XPATH,
                                                                      r'//*[contains(@data-ref-id, "address")]')])
        except Exception as ex:
            print(ex)
            address = ''
        return address



