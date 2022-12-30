
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

import time
import setting


class DominosParser():

    def __init__(self, post_code):
        self.post_code = post_code
        self.url = 'https://www.dominos.co.uk/'
        self.driver = None
        self.data_products = []
        self.data_parsed = []

        self.cards = None


        self.option_text = []

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
        time.sleep(1)
        self.close_popup()
        time.sleep(2)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()


    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']

        # I commented out the dominos proxy, since a different proxy is needed
        # options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
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



    def get_address(self):
        # $x('//span[@class="nav-store-name"]/ancestor::li')
        try:
            # self.driver.find_element(By.XPATH,
            #                     r'(//*[contains(text(), "Collection")]/ancestor::div/a)[1]').click()
            # $x('(//*[contains(text(), "Collection")]/ancestor::div[a])[1]')
            # $x('//*[contains(text(), "Collection")]/ancestor::div[contains(@class, "button-container")]')
            # url_address_info = self.driver.find_element(By.XPATH,
            #                     r'(//*[contains(text(), "Collection")]/ancestor::div/a)[1]').get_attribute('href')
            url_address_info = self.driver.current_url.replace('store', 'storefulfilment').replace('menu', 'moreinfo')
            print(url_address_info)

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

    def get_count_cards(self):
        self.cards = self.driver.find_elements(By.XPATH, r'//*[@data-ref-id="base-menu-item-container"]')
        count = len(self.cards)
        return count


    def get_current_html_card_by_element(self, index):
        # по ИД порядкового номера(от 0)
        return self.cards[index].get_attribute('outerHTML')
        # return self.cards[index].page_source
        # return self.driver.page_source
        # return self.driver.find_element(By.XPATH,  rf'(//*[@data-ref-id="base-menu-item-container"])[{index+1}]').get_attribute('outerHTML')
        # return self.driver.execute_script("return arguments[0].outerHTML;", self.cards[index])

    def scrolling_common(self, index):
        yield self.get_current_html_card_by_element(index)

    def scrolling_page(self, index):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.cards[index])
        time.sleep(1)

    def scrolling_select(self, index):
        try:
            select_size_options = self.cards[index].find_elements(By.XPATH,
                                                             './/div[contains(@class, "variants-container")]//select[@data-ref-id="base-select-input"]/option[not(@disabled="disabled")]')
            select_size = Select(self.cards[index].find_element(By.XPATH,
                                                           './/div[contains(@class, "variants-container")]//select[@data-ref-id="base-select-input"]'))

            self.option_text = [i.text for i in select_size_options]
            for option in select_size_options:
                print(f'option.text = {option.text}')
                select_size.select_by_visible_text(option.text)
                # self.option_text.append(option.text)
                time.sleep(0.8)
                yield self.get_current_html_card_by_element(index)
        except Exception as ex:
            # print(ex)
            yield False

    def get_option_select(self):
        options = self.option_text
        for option in options:
            yield option



    def scrolling_choose(self, index, check=False):
        try:

            # button_choose = self.cards[index].find_element(By.XPATH, r'.//*[contains(text(), "choose")]/ancestor::button[contains(@data-ref-id, "base-menu-card")]')
            # button_choose = self.cards[index].find_element(By.XPATH, r'.//button[contains(@class, "group-button")]//*[contains(text(), "choose")]/ancestor::button[contains(@data-ref-id, "base-menu-card")]')
            button_choose = self.cards[index].find_element(By.XPATH, r'.//*[contains(text(), "choose")]')
            # button_choose = self.cards[index].find_element(By.XPATH, r'.//button[4]')
            # button_choose = self.cards[index].find_element(By.XPATH, r'.//button[contains(@data-ref-id, "base-menu-card")]')
            # button_choose = self.cards[index].find_element(By.XPATH, r'.//*[contains(text(), "choose")]/ancestor::button[contains(@data-ref-id, "base-menu-card")]')
            # print(f'button_choose  - {bool(button_choose)}')


            if check:
                yield True


            self.driver.execute_script("arguments[0].click();", button_choose)
            # button_choose.click()
            time.sleep(2)
            # $x('(//*[@data-ref-id="base-menu-item-container"])[50]/following-sibling::section')
            xpath_section = f'(//*[@data-ref-id="base-menu-item-container"])[{index+1}]/following-sibling::section//section[@data-ref-id="base-grid"]/div'
            tray_cards = self.driver.find_elements(By.XPATH, xpath_section)
            # tray_cards = self.driver.find_elements(By.XPATH,
            #                                       f'//*[@data-ref-id="base-menu-item-container"]//section[contains(@class, "base-cards-tray")]//section/div')
            print(len(tray_cards))
            # time.sleep(3333)
            for tray_card in tray_cards:
                yield tray_card.get_attribute('outerHTML')
        except Exception as ex:
            yield False
        else:
            self.driver.execute_script("arguments[0].click();", button_choose)
            time.sleep(1)


    def get_type_card(self, index):

        select_type = bool(next(self.scrolling_select(index)))
        choose_type = bool(next(self.scrolling_choose(index, check=True)))
        type_card = {
                        True:'common_type',
                        select_type:'select_type',
                        choose_type:'choose_type',
                     }

        return type_card[True]

    def get_category(self, index):
        # $x('(//*[@data-ref-id="base-menu-item-container"])[1]/ancestor::section[@class="base-scroll-section"]')
        try:
            xpath = rf'(//*[@data-ref-id="base-menu-item-container"])[{index+1}]/ancestor::section[@class="base-scroll-section"]'
            category = self.driver.find_element(By.XPATH, xpath).get_attribute('id')
            return category
        except:
            return 'error'

    def find(self, index, xpath_collections, attribute = 'innerHTML'):
        data_set = ''
        for xpath in xpath_collections:
            try:
                xpath = rf'(//*[@data-ref-id="base-menu-item-container"])[{index+1}]{xpath[1:]}'
                html = self.driver.find_element(By.XPATH, xpath).get_attribute(attribute)
                # html = self.cards[index].find_element(By.XPATH, xpath).get_attribute(attribute)
                data_set += html
            except:
                data_set += 'error'
        return data_set

    def get_image(self, index):
        xpath_collections = (
            './/img',
            './/*[@loading="lazy"]',
            './/*[@class="base-lazy-image"]',
            './/picture',
        )
        html_collections = self.find(index, xpath_collections, 'src')
        return html_collections

    def get_price(self, index):
        xpath_collections = (
            './/*[contains(text(), "£")]',
            './/*[@data-ref-id="base-menu-price-text"]',
            './/*[contains(@*, "price")]',
        )
        html_collections = self.find(index, xpath_collections, 'textContent')
        return html_collections

    def get_name(self, index):
        xpath_collections = (
            './/*[contains(@*, "name")]',
            './/h3',
            './/*[contains(@*, "title")]',
        )
        html_collections = self.find(index, xpath_collections, 'textContent')
        return html_collections