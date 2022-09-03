import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import datetime
import pandas as pd

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
        self.voucher_codes_cards_data = []
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
        self.deals_cards_data = []
    def click_accept(self):
        try:
            self.driver.find_element(By.XPATH, '//*[contains(text(), "Accept")]').click()
            time.sleep(1)
        except:
            pass

    def click_voucher_codes(self):
        # $x('(//button[contains(text(),"Voucher Codes")])[1]')
        pass

    def click_deals(self):
        # $x('(//button[contains(text(),"Deals")])[1]')
        pass

    def get_voucher_codes_cards(self):
        # $x('//article[contains(@class, "voucher")]')
        pass

    def get_deals_cards(self):
        # $x('//article[contains(@class, "deal")]')
        pass


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
        DataBase().create_stg_table(data_frame= df, name_stg_table='STG_HOTUKDEALS_BURGERKING')
