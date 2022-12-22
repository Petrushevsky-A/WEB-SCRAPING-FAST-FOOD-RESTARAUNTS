from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from seleniumwire import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert


import time
import setting

import os
import zipfile

class DeliverooPriceParser():

    def __init__(self, url):
        self.url = url
        self.driver = None
        self.cards = None


    def __enter__(self):
        # Запуск браузера
        self.driver = self.run_browser()
        time.sleep(2)
        # открывает ссылку
        self.open_url(self.url)
        time.sleep(3)


        time.sleep(3333)

        # Подверджает куки
        self.accept_click()
        time.sleep(1)

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()


    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']


        PROXY_HOST = '196.18.165.20' # rotating proxy
        PROXY_PORT = '8000'
        PROXY_USER = 'qXkJ97'
        PROXY_PASS = 'UjNPey'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"23.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


        pluginfile = 'proxy_auth_plugin.zip'

        if True:
            pass
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)





        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        time.sleep(3)

        return driver


    def open_url(self, url):
        # url = r'https://qXkJ97:UjNPey@www.ubereats.com/store/mcdonalds-west-one-centre/Z-hqtVFgSFOaUUpAMcwcfw/404b1493-27cb-54b9-9978-5f3254d1c90d?diningMode=DELIVERY'
        self.driver.get(url=url)

        time.sleep(5)

    def accept_click(self):

        try:
            self.driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
            time.sleep(2)
        except:
            print("Not found accept")

    def scrolling_page(self, card):
        self.driver.execute_script("arguments[0].scrollIntoView();", card)
        time.sleep(0.2)

    def get_item_cards(self):
        cards = self.driver.find_elements(By.XPATH,  r'//li/div[contains(@class, "MenuItemCard")]')
        return cards

    def get_title_item(self, card):
        xpath = r'.//p[1]'
        try:
            item = card.find_element(By.XPATH, xpath)
            title = item.text
        except Exception as ex:
            print(ex)
            title = 'Not found'
        print(f'title {title}')
        return title

    def get_image_url(self, card):
        xpath = r'.//div[contains(@style, "background-image:")]'
        try:
            item = card.find_element(By.XPATH, xpath)
            image_url = item.get_attribute('style').replace('background-image: url("', '').replace('");', '')
        except Exception as ex:
            print(ex)
            image_url = 'Not found'

        print(f'image_url {image_url}')
        return image_url

    def get_description(self, card):
        xpath = r'.//span[1]'
        try:
            item = card.find_element(By.XPATH, xpath)
            description = item.text
        except Exception as ex:
            print(ex)
            description = 'Not found'
        print(f'description {description}')
        return description

    def get_price(self, card):
        xpath = r'.//span[contains(text(), "£")]'
        try:
            item = card.find_element(By.XPATH, xpath)
            price = item.text.replace('£', '')
        except Exception as ex:
            print(ex)
            price = 'Not found'
        print(f'price {price}')
        return price

    def get_calories(self, card):
        xpath = r'.//p[2]'
        try:
            item = card.find_element(By.XPATH, xpath)
            calories = item.text.replace(' kcal', '')
        except Exception as ex:
            print(ex)
            calories = 'Not found'
        print(f'calories {calories}')
        return calories

    def get_html_card(self, card):
        try:
            html = card.get_attribute('outerHTML')
        except Exception as ex:
            print(ex)
            html = 'Not found'
        print(f'html {html}')
        return html


    def get_category(self, card):
        xpath = r'./ancestor::div[contains(@id,"layout")]/div[@data-testid="layout-head"]//h3'
        try:
            item = card.find_element(By.XPATH, xpath)
            category = item.get_attribute('innerHTML')
        except Exception as ex:
            print(ex)
            category = 'Not found'
        print(f'category {category}')
        return category

    def get_address(self, city):
        try:
            # button
            xpath = r'//*[text()= "Info"]'
            item = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)

            # address
            xpath = rf'//span[contains(text(), "{city}")]'
            item = self.driver.find_element(By.XPATH, xpath)
            time.sleep(0.4)
            address = item.text
            print(f'address {address}')
        except Exception as ex:
            print(ex)
            address = 'Not found'

        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
        except Exception as ex:
            print(ex)

        return address

    def get_post_code(self, address):
        try:
            post_code = address.split(',')[-1].strip()
        except Exception as ex:
            print(ex)
            post_code = 'Not found'
        return post_code
