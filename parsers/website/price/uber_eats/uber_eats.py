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
        print('__enter__')
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)

        self.driver.implicitly_wait(5)

        self.open_url(self.url)
        self.close_modal_window()

        self.accept_click()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        self.driver.close()
        self.driver.quit()

    def open_url(self, url):
        print('open_url')
        self.driver.get(url=url)
        time.sleep(5)

    def close_modal_window(self):
        print('close_modal_window')
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
        print('accept_click')
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
        print('open_item_card')
        xpath = rf'(//li/ul/li)[{id_card}]'
        card = self.driver.find_element(By.XPATH, xpath)
        card.click()
        print('open card')
        time.sleep(4)

    def navigate_back(self):
        self.driver.back()
        time.sleep(7)

    def get_address(self):
        print('get_address')
        self.open_more_info()
        try:
            xpath = r'//div[@role="dialog"]//button//div[contains(text(), ",")]'
            self.address = self.driver.find_element(By.XPATH, xpath).text
            self.close_modal_window()
        except Exception as ex:
            print(ex)
            self.address = 'Not found'
        finally:
            return self.address

    def open_more_info(self):
        print('open_more_info')
        try:
            xpath = r'//*[text() = "More info"]'
            element = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script('arguments[0].click();', element)
        except Exception as ex:
            print(ex)
        finally:
            time.sleep(2)


    def get_category(self, id_card):
        print('get_category')
        xpath = rf'(//li/ul/li)[{id_card}]/ancestor::li/div[1]'
        try:
            category = self.driver.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            category = 'Not found'
        finally:
            return category

    def get_image_url(self):
        print('get_image_url')
        xpath = r'//img[@role="presentation"]'
        try:
            image_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        except Exception as ex:
            print(ex)
            image_url = 'Not found'
        finally:
            return image_url

    def get_description(self):
        # '//h1/parent::div/parent::div//div[string-length(text())>20]'
        # '(//div[string-length(text())>20])[1]'
        xpath = r'//div[child::h1]/div/div'
        try:
            self.driver.refresh()
            description = self.driver.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            description = 'Not found'
        finally:
            return description

    def get_title_item(self):
        print('get_title_item')
        xpath = r'//h1'
        try:
            title = self.driver.find_element(By.XPATH, xpath).text
        except Exception as ex:
            print(ex)
            title = 'Not found'
        finally:
            return title


    # temp sctipt
    def size(self):
        xpath = r'//li[descendant::div[contains(text(), "Size")]]//label'
        try:

            self.sizes_button = self.driver.find_elements(By.XPATH, xpath)
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


    def get_size_element(self, size):
        try:
            xpath = r'.//div[text()][1]'
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
            xpath = r'.//div[contains(text(), "£")]'
            price_element = size.find_element(By.XPATH, xpath)
            price = price_element.text.replace('£', '')
            price = float(price)

            print(f'price size {price}')
        except Exception as ex:
            print(ex)
            price = 0
        finally:
            self.prices.append(self.base_price + price)



    # делаю
    def get_calories(self):
        print('get_calories')
        xpath = r'//div[contains(text(), "kcal")]'
        try:
            calories = self.driver.find_element(By.XPATH, xpath).text
            calories.replace(' kcal', '')
        except Exception as ex:
            print(ex)
            calories = 'Not found'
        finally:
            return calories


    def get_html_card(self):
        print('get_html_card')
        xpath = r'//main/div[1]/div[1]'
        try:
            html_card = self.driver.find_element(By.XPATH, xpath).get_attribute('outerHTML')
        except Exception as ex:
            print(ex)
            html_card = 'Not found'
        finally:
            return html_card


    def get_base_price(self):
        xpath = r'//span[contains(text(), "£")]'
        try:
            price = self.driver.find_element(By.XPATH, xpath)
            price = price.text.replace('£', '')
            self.base_price = float(price)
        except Exception as ex:
            print(ex)
            price = 'Not found'
            self.base_price = 0
        # print(f'price {price}')


    def get_post_code(self, address):
        try:
            post_code = address.split(',')[-1].strip()
        except:
            post_code = 'Not found'
        finally:
            return post_code


    def get_head(self):
        xpath = r'(//h1)[last()]'
        try:
            head = self.driver.find_element(By.XPATH, xpath).text
        except:
            head = 'Not found'
        finally:
            return head
    def get_brand(self):
        xpath = r'(//h1)[last()]'
        try:
            brand = 'Not found'
        except:
            brand = 'Not found'
        finally:
            return brand