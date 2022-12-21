# from selenium import webdriver
from seleniumwire import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
# import undetected_chromedriver.v2 as undetected_chrome
# import seleniumwire.undetected_chromedriver.v2 as uc


# from selenium.webdriver import DesiredCapabilities

import time
# from datetime import datetime
# from multiprocessing import Pool
# import pandas as pd


# from database.database import DataBase
import setting


class UberEatsPriceParser():

    def __init__(self, url):
        self.driver = None
        self.url = url


    def __enter__(self):
        # options = Options()
        options = Options()
        # options = uc.ChromeOptions()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']

        # options.binary_location = '/usr/bin/google-chrome-stable'
        # tuple(map(lambda x: options.add_experimental_option(*x), setting.EXPERIMENTAL_OPTION_SELENIUM.items()))

        # options.add_argument(ua.chrome)
        # caps = options.to_capabilities()
        # caps["acceptInsecureCerts"] = True
        # options.add_argument('--ignore-certificate-errors-spki-list')
        # options.add_argument('--no-zygote')
        # options.add_argument('--log-level=3')
        # options.add_argument('--allow-running-insecure-content')
        # options.add_argument('--disable-web-security')
        # options.add_argument('--disable-features=VizDisplayCompositor')
        # options.add_argument('--disable-breakpad')
        # capabilities = DesiredCapabilities.CHROME.copy()
        # capabilities["acceptInsecureCerts"] = True
        # capabilities["acceptSslCerts"] = True
        # options.set_capability("acceptInsecureCerts", True)
        # options.add_argument('--allow-insecure-localhost')  # differ on driver version. can ignore.
        # caps = options.to_capabilities()
        # caps["acceptInsecureCerts"] = True
        # webdriver.Chrome()
        # options.binary_location = r'/usr/bin/google-chrome-stable'
        # options.binary_location = r'/usr/bin/google-chrome'
        # options.binary_location = r'/usr/bin/chromium'
        options.binary_location = r'/opt/google/chrome/chrome'
        # self.driver = webdriver.Chrome(chrome_options=options, executable_path=path, seleniumwire_options=setting.PROXY_SELENIUMWIRE, desired_capabilities=capabilities)
        # options.set_headless(True)
        # options.add_argument('--profile-directory=Default')
        # ch_options.add_argument("user-data-dir = /path/to/Chrome Profile")
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path, seleniumwire_options=setting.PROXY_SELENIUMWIRE)
        # self.driver = webdriver.Firefox(options=options, executable_path=path, seleniumwire_options=setting.PROXY_SELENIUMWIRE, desired_capabilities=capabilities)
        # self.driver = uc.Chrome(seleniumwire_options=setting.PROXY_SELENIUMWIRE)
        # self.driver = uc.Chrome()


        self.open_url(self.url)
        self.accept_click()
        self.close_modal_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()

    def open_url(self, url):
        self.driver.get(url=url)
        time.sleep(5)

    def close_modal_window(self):
        (ActionChains(self.driver)
            .send_keys(Keys.ESCAPE)
            .send_keys(Keys.ESCAPE)
            .send_keys(Keys.ESCAPE)
            .perform())
        time.sleep(1)

    def accept_click(self):
        try:
            self.driver.find_element(By.XPATH, r'//button[contains(text(), "Accept")]').click()
            time.sleep(1)
        except Exception as ex:
            print(ex)
    def get_items(self):
        '//li/ul/li'
        print(123)

    def get_category(self):
        '//li/ul/li/ancestor::li/div[1]'

    def get_modal_window_item_info(self):
        '//div[@role="dialog"]'

    def get_image_url(self):
        '//div[@role="dialog"]//img'

    def get_description(self):
        '//div[@role="dialog"]//h1/following-sibling::div/div'

    def get_head(self):
        '//div[@role="dialog"]//h1'
        '//div[@role="dialog"]//h2'

    def get_price(self):
        '//div[@role="dialog"]//*[contains(text(), "€")]'

    def get_size(self):
        pass
    def open_item_card(self):
        # '//*[text() = "Quick view"]'
        self.driver.find_element(By.XPATH, r'//button[contains(text(), "Accept")]')