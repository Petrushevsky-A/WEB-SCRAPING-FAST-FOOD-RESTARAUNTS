import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import setting
from database.database import DataBase
from ...parser import Parser

class HotukdealsParser(Parser):

    def __init__(self, url):


        self.driver = None
        self.url = url






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
        list_cards = [i.get_attribute('outerHTML') for i in self.driver.find_elements(By.XPATH, '//article[contains(@class, "voucher")]')]
        return pd.DataFrame({'voucher_codes_card': list_cards})


    def get_deals_cards(self):
        # $x('//article[contains(@class, "deal")]')
        list_cards = [i.get_attribute('outerHTML') for i in
                      self.driver.find_elements(By.XPATH, '//article[contains(@class, "deal")]')]

        return pd.DataFrame({'deals_card': list_cards})




    def get_deals_page(self):

        # $x('//div[contains(@class,  "thread--deal")]//img')
        list_image = ' '.join(self.finds('//div[contains(@class,  "thread--deal")]//img', method='get_attribute', method_arguments='src'))
        # $x('//h1')
        head = self.find('//h1', attribute='text')
        # $x('//div[contains(@id,"thread")]//span[contains(@class,  "price")]')
        price = self.find('//div[contains(@id,"thread")]//span[contains(@class,  "price")]', attribute='text')
        # $x('//div[contains(@id,"thread")]//span[contains(@class,  "brandPrimary")]')
        brand = self.find('//div[contains(@id,"thread")]//span[contains(@class,  "brandPrimary")]', attribute='text')
        # # $x('//div[contains(@id,"thread")]//span[contains(@class,  "cept-vote-temp vote-temp vote-temp--burn")]').map(i=>i.textContent)
        vote = self.find('//div[contains(@id,"thread")]//span[contains(@class,  "cept-vote-temp vote-temp vote-temp--burn")]', 'innerHTML')
        # # $x('//div[contains(@class,"cept-thread-content")]//span[contains(text(),  "Posted")]').map(i=>i.textContent)
        date = self.find('//div[contains(@class,"cept-thread-content")]//span[contains(text(),  "Posted")]', 'text')
        # # $x('//div[contains(@class,"cept-thread-content")]//div[contains(@class,  "threadUpdate")]').map(i=>i.textContent)
        date_update = self.find('//div[contains(@class,"cept-thread-content")]//div[contains(@class,  "threadUpdate")]', 'text')
        # # $x('//div[contains(@class,"cept-thread-content")]//div[contains(@class,  "content ")]').map(i=>i.textContent)
        content = ' '.join(self.finds('//div[contains(@class,"cept-thread-content")]//div[contains(@class,  "content ")]', 'text'))
        data = {
            'list_image':list_image,
            'head':head,
            'price':price,
            'brand':brand,
            'vote':vote,
            'date':date,
            'date_update':date_update,
            'content':content,
        }
        return pd.DataFrame([data])


    def get_voucher_codes_page(self):
        # $x('//div[contains(@class, "cept-thread-content")]//img')
        list_image = ' '.join(self.finds('//div[contains(@class, "cept-thread-content")]//img', method='get_attribute', method_arguments='src'))
        # # $x('//h1')
        head = self.find('//h1', 'text')
        # $x('//span[contains(@class, "thread-price")]/span[contains(text(), "£")]')
        price = self.find('//span[contains(@class, "thread-price")]/span[contains(text(), "£")]', 'text')
        # $x('//span[contains(@class, "brandPrimary  ")]')
        brand = self.find('//span[contains(@class, "brandPrimary  ")]', 'text')
        # $x('//span[contains(@class, "cept-vote-temp")]')
        vote = self.find('//span[contains(@class, "cept-vote-temp")]', 'text')
        # $x('//div[contains(@class, "orangePale")]')
        date = self.find('//div[contains(@class, "orangePale")]', 'text')

        # $x('//div[contains(@class, "cept-thread-content")]')
        content = ' '.join(self.finds('//div[contains(@class, "cept-thread-content")]', 'text'))

        data = {
            'list_image': list_image,
            'head': head,
            'price': price,
            'brand': brand,
            'vote': vote,
            'date': date,
            'content': content,
        }
        return pd.DataFrame([data])



    def see_more_voucher_codes_page(self):
        # $x('//*[contains(text(), "See More")]')
        # $x('//button[@data-t="seeMoreVouchersButton"]')
        # $x('//button[@data-t="seeMoreDealsButton"]')
        # self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element('//button[@data-t="seeMoreVouchersButton"]'))
        self.find('//button[@data-t="seeMoreVouchersButton"]', method='click')

    def see_more_deals_cards_page(self):
        # $x('//*[contains(text(), "See More")]')
        # $x('//button[@data-t="seeMoreVouchersButton"]')
        # $x('//button[@data-t="seeMoreDealsButton"]')
        # self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element('//button[@data-t="seeMoreVouchersButton"]'))
        self.find('//button[@data-t="seeMoreDealsButton"]', method='click')
