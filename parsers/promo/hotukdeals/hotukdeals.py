import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import setting
from database.database import DataBase

class HotukdealsParser():

    def __init__(self):


        self.driver = self.run_browser()
        self.click_accept()
        # [
        #   {
        #       'box':
        #       'head':
        #       'expires':
        #       'voucher':
        #       'more info':
        #       'last used':
        #       'url_site_brand':
        #       'url_voucher_page':
        #   },
        #   {...},
        #   ...
        # ]
        self.voucher_codes_cards_data = self.get_voucher_codes_cards()
        # [
        #   {
        #       'image':
        #       'head':
        #       'vote':
        #       'expires':
        #       'date_posted':
        #       'update':
        #       'price':
        #       'description':
        #       'url_site_brand':
        #       'url_voucher_page':
        #   },
        #   {...},
        #   ...
        # ]
        self.deals_cards_data = self.get_deals_cards()
        self.to_stg_db()

        self.driver.close()
        self.driver.quit()


    def click_accept(self):
        try:
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Accept")]').click()
            time.sleep(2)
        except:
            pass

    def click_voucher_codes(self):
        # $x('(//button[contains(text(),"Voucher Codes")])[1]')
        self.driver.find_element(By.XPATH, '(//button[contains(text(),"Voucher Codes")])[1]').click()
        pass

    def click_deals(self):
        # $x('(//button[contains(text(),"Deals")])[1]')
        self.driver.find_element(By.XPATH, '(//button[contains(text(),"Deals")])[1]').click()
        pass

    def get_voucher_codes_cards(self):
        # $x('//article[contains(@class, "voucher")]')
        list_cards = [i.get_attribute('innerHTML') for i in self.driver.find_elements(By.XPATH, '//article[contains(@class, "voucher")]')]
        return pd.DataFrame({'voucher_codes_card': list_cards})


    def get_deals_cards(self):
        # $x('//article[contains(@class, "deal")]')
        list_cards = [i.get_attribute('innerHTML') for i in
                      self.driver.find_elements(By.XPATH, '//article[contains(@class, "deal")]')]
        return pd.DataFrame({'deals_card': list_cards})


    def get_voucher_codes_page(self):
        pass

    def get_deals_page(self):
        pass

    def save_image(self):
        pass


    def run_browser(self):

        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']

        url = 'https://www.hotukdeals.com/vouchers/burgerking.co.uk'

        driver = webdriver.Chrome(chrome_options=options, executable_path=path)

        time.sleep(2)
        driver.get(url=url)
        time.sleep(5)

        return driver

    def to_stg_db(self):
        # DataBase().create_stg_table(data_frame= self.get_deals_cards, name_stg_table='STG_HOTUKDEALS_BURGERKING')
        print(type(self.deals_cards_data))
        DataBase().create_stg_table(data_frame= self.deals_cards_data, name_stg_table='STG_HOTUKDEALS_BURGERKING_DEALS_CARDS')
