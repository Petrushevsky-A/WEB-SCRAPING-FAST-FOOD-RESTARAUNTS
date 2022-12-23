import time
import itertools

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import datetime
import pandas as pd


from database.database import DataBase

import setting

class UberEatsPromoParser():


        def __init__(self, post_code):
                self.post_code = post_code
                self.url = r'https://www.ubereats.com/gb'
                self.driver = None
                self.cards = []


        def __enter__(self):
                self.driver = self.run_browser()
                time.sleep(2)
                self.open_url(self.url)
                time.sleep(3)
                self.set_search()
                time.sleep(3)
                self.accept_click()
                time.sleep(1)
                self.set_filter()
                time.sleep(3)
                self.scrolling_to_bottom()
                time.sleep(3)
                self.get_cards()
                time.sleep(3)
                return self

        def __exit__(self, exc_type, exc_val, exc_tb):
                self.driver.close()
                self.driver.quit()

        def run_browser(self):
                options = Options()
                tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
                path = setting.SELENIUM['path']
                options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
                driver = webdriver.Chrome(chrome_options=options, executable_path=path)
                return driver

        def open_url(self, url):
                self.driver.get(url=url)
                time.sleep(5)

        def set_search(self):
                # set input
                self.driver.find_element(By.XPATH, '//input[@name="searchTerm"]').send_keys(f'{self.post_code}')
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//input[@name="searchTerm"]').send_keys(Keys.ENTER)
                time.sleep(8)

        def accept_click(self):

                try:
                        self.driver.find_element(By.XPATH, '//div[@id="cookie-banner"]//button[text() = "Accept"]').click()
                        time.sleep(1)
                except:
                        pass

        def set_filter(self):
                try:
                        self.driver.find_element(By.XPATH,
                                            '//div[contains(@class,"aw")]/parent::div/preceding-sibling::div//div[text() = "Deals"]').click()
                        time.sleep(5)
                except:
                        pass

        def scrolling_to_bottom(self):
                for i in range(30):
                        try:
                                self.driver.find_element(By.XPATH, '//button[text() = "Show more"]').click()
                                time.sleep(4)
                        except:
                                break
                self.cards = self.driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div')
                for element in self.cards:
                        self.driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(0.15)

        def get_cards(self):
                xpath = '//div[@data-test="feed-desktop"]/div'
                self.cards = self.driver.find_elements(By.XPATH, xpath)

        def get_html(self, index):
                try:
                        return self.cards[index].get_attribute('outerHTML')
                except:
                        return 'Not Found'

        def get_image(self, index):
                try:
                        src = self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                        print(src)
                        return src
                except:
                        return 'Not Found'

        def get_head(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/h3').text
                except:
                        return 'Not Found'


        def get_description(self, index):
                xpath = r'.//picture/parent::div/following-sibling::div/div[1]'
                try:
                        return self.cards[index].find_elements(By.XPATH, xpath)[0].text
                except:
                        return 'Not Found'


        def get_prices(self, index):
                xpath = r'.//span[contains(text(), "£")]'
                try:
                        # No delivery partners nearby
                        return self.cards[index].find_element(By.XPATH, xpath).text
                except:
                        return 'Not Found'


        def get_times(self, index):
                xpath = r'.//div[contains(text(), "min")]'
                try:
                        return self.cards[index].find_element(By.XPATH, xpath).text
                except:
                        return 'Not Found'


        def get_rating(self, index):
                xpath = r'.//span[contains(text(), "rated")]'
                try:
                        return self.cards[index].find_element(By.XPATH, xpath).text
                except:
                        return 'Not Found'

