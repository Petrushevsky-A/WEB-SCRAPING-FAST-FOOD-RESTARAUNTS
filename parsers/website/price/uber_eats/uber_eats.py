from datetime import date

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

import time

import setting



class UberEatsPriceParser():

    def __init__(self, url):
        self.driver = None
        self.url = url


        self.address = ''
        self.image_url = ''

        self.base_price = None
        self.sizes = []
        self.prices = []

        self.sizes_button = None

    def __enter__(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)

        self.open_url(self.url)
        self.close_modal_window()

        # self.get_address()

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

    def scrolling_to_card(self, id_card):
        time.sleep(2)
        xpath = rf'(//li/ul/li)[{id_card}]'
        card = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("scroll(0, 250);")
        time.sleep(1)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
        time.sleep(0.2)

    def accept_click(self):
        try:
            self.driver.find_element(By.XPATH, r'//button[contains(text(), "Accept")]').click()
            time.sleep(1)
        except Exception as ex:
            print(ex)

    def get_count_items(self):
        print('get count items card')
        xpath = r'//li/ul/li'
        cards = self.driver.find_elements(By.XPATH, xpath)
        time.sleep(1)
        count_cards = len(cards)
        return count_cards

    def open_item_card(self, id_card):
        xpath = rf'(//li/ul/li)[{id_card}]'
        card = self.driver.find_element(By.XPATH, xpath)
        card.click()
        print('open card')
        time.sleep(4)

    def navigate_back(self):
        self.driver.back()
        time.sleep(7)

    def get_address(self):
        self.open_more_info()
        xpath = r'//div[@role="dialog"]//button//div[contains(text(), ",")]'
        self.address = self.driver.find_element(By.XPATH, xpath).text
        self.close_modal_window()

    def open_more_info(self):
        try:
            xpath = r'//*[text() = "More info"]'
            self.driver.find_element(By.XPATH, xpath).click()
        except:
            pass

    # ========================================================================================================
    # parse size

    def quik_button(self, card):
        xpath = r'.//*[text() = "Quick view"]'
        try:
            card.find_element(By.XPATH, xpath).click()
        except Exception as ex:
            print(ex)

    # cghange cpath
    def get_category(self, card):
        xpath = r'//li/ul/li/ancestor::li/div[1]'
        try:
            category = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            category = 'Not found'
        finally:
            return category

    def get_image_url(self):
        xpath = r'//div[@role="dialog"]//img'
        try:
            image_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        except Exception as ex:
            print(ex)
            image_url = 'Not found'
        finally:
            return image_url

    def get_description(self, card):
        xpath = r'//h1/parent::div/parent::div//div[contains(text(), ".")]'
        try:
            description = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            description = 'Not found'
        finally:
            return description

    def get_title_item(self):
        xpath = r'.//h1'
        try:
            title = self.driver.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            title = 'Not found'
        finally:
            return title

    def get_price(self, card):
        xpath = './/div[@role="dialog"]//*[contains(text(), "£")]'
        try:
            price = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            price = 'Not found'
        finally:
            return price

    # temp sctipt
    def modal_window(self, card):
        # $x('//div[@class="ReactModalPortal"]/div//p[contains(text(),"Size")]/following-sibling::div//button//div[contains(@class, "MenuItemModifiers")]/span')
        try:
            self.click_card(card)
            self.sizes_button = self.driver.find_elements(By.XPATH,
                                                          '//div[@class="ReactModalPortal"]/div//p[contains(text(),"Size")]/following-sibling::div//button')

            if not self.sizes_button:
                raise
            print('=' * 33)
            for size in self.sizes_button:
                self.get_size_element(size)
                self.get_prices_modal_windows(size)
            print('=' * 33)
        except Exception as ex:
            print(ex)
            self.sizes.append('')
            self.prices.append(self.base_price)
        else:
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def get_size_element(self, size):
        try:
            xpath = r'.//p'
            size_name_element = size.find_element(By.XPATH, xpath)
            size_name = size_name_element.text

            print(f'size_name.text {size_name}')
        except Exception as ex:
            print(ex)
            size_name = ''
        finally:
            self.sizes.append(size_name)

    def get_prices_modal_windows(self, size):
        try:
            xpath = r'.//span[contains(text(), "+")]'
            price_element = size.find_element(By.XPATH, xpath)
            price = price_element.text.replace('+£', '')
            price = float(price)

            print(f'price size {price}')
        except Exception as ex:
            print(ex)
            price = 0
        finally:
            self.prices.append(self.base_price + price)

    # ==========================================================================================================
    def scrolling_page(self):
        time.sleep(15)
        for i in range(30):
            print('Page down')
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

    # делаю
    def get_calories(self):
        pass

    def get_html_card(self, card):
        try:
            html_card = card.get_attribute('outerHTML')
        except Exception as ex:
            print(ex)
            html_card = 'Not found'
        finally:
            return html_card









# ===============================================================================================================
class UberEatsPriceParser_OLD():

    def __init__(self, url):
        self.driver = None
        self.url = url
        # self.post_code = post_code
        # self.brand = brand

        self.address = ''
        self.image_url = ''

        self.base_price = None
        self.sizes = []
        self.prices = []

        self.sizes_button = None

    def __enter__(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        # prefs = {"profile.default_content_setting_values.geolocation": 2}
        # options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)

        self.open_url(self.url)
        # self.open_place()
        # time.sleep(3333)
        self.close_modal_window()

        # self.get_address()

        # time.sleep(3333)
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

    def open_place(self):
        url = r'https://www.ubereats.com/'
        self.open_url(url)
        self.accept_click()
        # set search request
        xpath = r'//input[@name="searchTerm"]'
        input = self.driver.find_element(By.XPATH, xpath)
        input.send_keys(self.post_code)
        time.sleep(2)

        # click first
        # xpath = r'//ul[@id="location-typeahead-home-menu"]/li[1]'
        # first_element_li = self.driver.find_element(By.XPATH, xpath)
        # first_element_li.click()
        # time.sleep(2)

        input.send_keys(Keys.ENTER)
        time.sleep(7)

        xpath = r'//input'
        input = self.driver.find_element(By.XPATH, xpath)
        input.send_keys(self.brand)
        time.sleep(4)

        xpath = r'//li[@id = "search-suggestions-typeahead-item-0"]/a'
        hint = self.driver.find_element(By.XPATH, xpath)
        hint.click()
        time.sleep(6)

    def scrolling_to_card(self, id_card):
        time.sleep(2)
        xpath = rf'(//li/ul/li)[{id_card}]'
        card = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("scroll(0, 250);")
        time.sleep(1)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
        time.sleep(0.2)

    def accept_click(self):
        try:
            self.driver.find_element(By.XPATH, r'//button[contains(text(), "Accept")]').click()
            time.sleep(1)
        except Exception as ex:
            print(ex)

    def get_count_items(self):
        print('get count items card')

        xpath = r'//li/ul/li'
        cards = self.driver.find_elements(By.XPATH, xpath)
        time.sleep(1)
        count_cards = len(cards)
        return count_cards

    def open_item_card(self, id_card):

        xpath = rf'(//li/ul/li)[{id_card}]'
        card = self.driver.find_element(By.XPATH, xpath)
        card.click()
        print('open card')
        time.sleep(4)
        # try:
        #     xpath = r'//*[text() = "Quick view"]'
        #     self.cards = self.driver.find_elements(By.XPATH, xpath)
        # except Exception as ex:
        #     print(ex)

    def navigate_back(self):
        self.driver.back()
        time.sleep(7)

    def get_address(self):
        self.open_more_info()
        xpath = r'//div[@role="dialog"]//button//div[contains(text(), ",")]'
        self.address = self.driver.find_element(By.XPATH, xpath).text
        self.close_modal_window()

    def open_more_info(self):
        try:
            xpath = r'//*[text() = "More info"]'
            self.driver.find_element(By.XPATH, xpath).click()
        except:
            pass

    # ========================================================================================================
    # parse size

    def quik_button(self, card):
        xpath = r'.//*[text() = "Quick view"]'
        try:
            card.find_element(By.XPATH, xpath).click()
        except Exception as ex:
            print(ex)

    # cghange cpath
    def get_category(self, card):
        xpath = r'//li/ul/li/ancestor::li/div[1]'
        try:
            category = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            category = 'Not found'
        finally:
            return category

    def get_image_url(self):
        xpath = r'//div[@role="dialog"]//img'
        try:
            image_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        except Exception as ex:
            print(ex)
            image_url = 'Not found'
        finally:
            return image_url

    def get_description(self, card):
        xpath = r'//h1/parent::div/parent::div//div[contains(text(), ".")]'
        try:
            description = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            description = 'Not found'
        finally:
            return description

    def get_title_item(self):
        xpath = r'.//h1'
        try:
            title = self.driver.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            title = 'Not found'
        finally:
            return title

    def get_price(self, card):
        xpath = './/div[@role="dialog"]//*[contains(text(), "£")]'
        try:
            price = card.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            price = 'Not found'
        finally:
            return price

    # temp sctipt
    def modal_window(self, card):
        # $x('//div[@class="ReactModalPortal"]/div//p[contains(text(),"Size")]/following-sibling::div//button//div[contains(@class, "MenuItemModifiers")]/span')
        try:
            self.click_card(card)
            self.sizes_button = self.driver.find_elements(By.XPATH,
                                                          '//div[@class="ReactModalPortal"]/div//p[contains(text(),"Size")]/following-sibling::div//button')

            if not self.sizes_button:
                raise
            print('=' * 33)
            for size in self.sizes_button:
                self.get_size_element(size)
                self.get_prices_modal_windows(size)
            print('=' * 33)
        except Exception as ex:
            print(ex)
            self.sizes.append('')
            self.prices.append(self.base_price)
        else:
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def get_size_element(self, size):
        try:
            xpath = r'.//p'
            size_name_element = size.find_element(By.XPATH, xpath)
            size_name = size_name_element.text

            print(f'size_name.text {size_name}')
        except Exception as ex:
            print(ex)
            size_name = ''
        finally:
            self.sizes.append(size_name)

    def get_prices_modal_windows(self, size):
        try:
            xpath = r'.//span[contains(text(), "+")]'
            price_element = size.find_element(By.XPATH, xpath)
            price = price_element.text.replace('+£', '')
            price = float(price)

            print(f'price size {price}')
        except Exception as ex:
            print(ex)
            price = 0
        finally:
            self.prices.append(self.base_price + price)

    # ==========================================================================================================
    def scrolling_page(self):
        time.sleep(15)
        for i in range(30):
            print('Page down')
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

    # делаю
    def get_calories(self):
        pass

    def get_html_card(self, card):
        try:
            html_card = card.get_attribute('outerHTML')
        except Exception as ex:
            print(ex)
            html_card = 'Not found'
        finally:
            return html_card



