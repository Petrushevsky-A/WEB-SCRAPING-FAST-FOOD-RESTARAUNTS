import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import setting
from database.database import DataBase



class HotukdealsParser():

    def __init__(self, url):


        self.driver = None
        self.url = url


    def __enter__(self):
        self.driver = self.run_browser()
        time.sleep(2)
        self.open_url()
        time.sleep(3)

        self.click_accept()
        time.sleep(1)
        self.login()
        time.sleep(2)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    #     self.driver.close()
    #     self.driver.quit()
    #     return True

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
        list_cards = [i.get_attribute('outerHTML') for i in self.driver.find_elements(By.XPATH, '//article[contains(@class, "voucher")]')]
        return pd.DataFrame({'voucher_codes_card': list_cards})


    def get_deals_cards(self):
        # $x('//article[contains(@class, "deal")]')
        list_cards = [i.get_attribute('outerHTML') for i in
                      self.driver.find_elements(By.XPATH, '//article[contains(@class, "deal")]')]

        return pd.DataFrame({'deals_card': list_cards})


    def find(self, xpath, attribute = None, method= None, method_arguments = None):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if attribute:
                return element.__getattribute__(attribute)
            if method and method_arguments:
                return element.__getattribute__(method)(method_arguments)
            if method:
                return element.__getattribute__(method)()
        except Exception as ex:
            print(ex)
            return 'Not faund'


    def finds(self, xpath, attribute = None, method= None, method_arguments = None):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if attribute:
                return [i.__getattribute__(attribute) for i in elements]
            if method and method_arguments:
                return [i.__getattribute__(method)(method_arguments) for i in elements]
            if method:
                return [i.__getattribute__(method)() for i in elements]
        except Exception as ex:
            print(ex)
            return ['Not faund', ]

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

    def save_image(self):
        pass


    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        return driver

    def open_url(self, url=None):
        time.sleep(2)
        if url:
            self.driver.get(url=url)
        else:
            self.driver.get(url=self.url)
        time.sleep(5)






    def login(self):
        # Для успешного парсинга необходимо быть авторизованным,
        # иначе некоторые данные могут быть не собраны.

        email = "pbksiu9luy@paperpapyrus.com"
        login = "Pud123ddd"
        password = "qwerty123dD"
        # $x('//*[contains(text(), "Log in")]')
        self.driver.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()

        time.sleep(2)
        # $x('//input[contains(@id,"identity")]')
        self.driver.find_element(By.XPATH, '//input[contains(@id,"identity")]').send_keys(login)
        # $x('//input[contains(@id,"password")]')
        self.driver.find_element(By.XPATH, '//input[contains(@id,"password")]').send_keys(password)
        # $x('//button[contains(text(), "Log In")]')
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Log In")]').click()
        pass


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
