from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import setting
import time


class DominosPromoParser():
        def __init__(self, post_code):
                self.post_code = post_code
                self.url = r'https://www.dominos.co.uk/mydominos/login'
                self.driver = None
                self.image = None
                self.address = None
                self.card_deals = None
                self.cards_tray_image = None


        def __enter__(self):
                self.driver = self.run_browser()
                time.sleep(2)
                self.open_url(self.url)
                time.sleep(3)

                self.accept_click()
                time.sleep(1)
                self.login()
                time.sleep(3)

                self.open_address_info()
                self.address = self.get_address()
                time.sleep(1)
                self.change_store()
                self.set_post_code()
                time.sleep(1)
                self.click_first_button_list()
                time.sleep(1)
                self.open_deals()
                time.sleep(5)
                # time.sleep(3333)
                return self

        def __exit__(self, exc_type, exc_val, exc_tb):
                self.driver.close()
                self.driver.quit()

        def run_browser(self):
                options = Options()
                tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
                path = setting.SELENIUM['path']
                driver = webdriver.Chrome(chrome_options=options, executable_path=path)
                return driver

        def open_url(self, url):
                self.driver.get(url=url)
                time.sleep(5)

        def accept_click(self):
                try:
                    self.driver.find_element(By.XPATH, r'//button[contains(text(), "Accept")]').click()
                    time.sleep(2)
                except:
                    print("Not found accept")

        def click_first_button_list(self):
                try:
                    self.driver.find_element(By.XPATH, r'//*[contains(text(), "Collect")]/ancestor::button').click()
                    time.sleep(4)
                except:
                    print("not found button collect")

        def login(self):
                login = 'projectlondon2022@protonmail.com'
                password = 'Projectplaner123!'
                self.driver.find_element(By.XPATH, r'//div[@data-ref-id="login-email"]/input').send_keys(f'{login}')
                time.sleep(1)
                self.driver.find_element(By.XPATH, r'//div[@data-ref-id="login-password"]/input').send_keys(f'{password}')
                time.sleep(1)
                self.driver.find_element(By.XPATH, r'//button[@data-ref-id="login-btn"]').click()
                time.sleep(5)

        def open_address_info(self):
                time.sleep(1)
                href = self.driver.find_element(By.XPATH,
                                                r'//button[contains(@*,"navigation")]/following-sibling::div/a').get_attribute(
                    'href')
                print(href)
                time.sleep(1)
                self.open_url(href)
                time.sleep(5)

        def get_address(self):
                try:
                    # $x('//*[contains(@data-ref-id, "address")]')
                    address = ", ".join([i.text for i in self.driver.find_elements(By.XPATH,
                                                                                   r'//*[contains(@data-ref-id, "address")]')])
                except Exception as ex:
                    # print(ex)
                    address = ''
                # print(address)
                return address

        def change_store(self):
                self.driver.find_element(By.XPATH, '//button[@data-ref-id="changeStoreButton"]').click()

        def set_post_code(self):
                # $x('//input[contains(@aria-label, "postcode")]')
                time.sleep(3)
                xpath_set = (
                    r'//input[contains(@aria-label, "postcode")]',
                    r'//input[contains(@data-ref-id, "base-input")]',
                    r'//input',
                )
                for xpath in xpath_set:
                    try:
                        # print(xpath)
                        input_element = self.driver.find_element(By.XPATH, xpath)
                        break
                    except:
                        continue
                input_element.send_keys(self.post_code)
                time.sleep(0.3)
                input_element.send_keys(Keys.ENTER)
                time.sleep(5)

        def click_first_button_list(self):
                try:
                    self.driver.find_element(By.XPATH, r'//*[contains(text(), "Collect")]/ancestor::button').click()
                    time.sleep(4)
                except:
                    print("not found button collect")

        def open_deals(self):
                curent_url = self.driver.current_url
                curent_url = curent_url.replace('menu', 'deals')
                self.open_url(curent_url)
                time.sleep(5)
                # print(curent_url)

        def get_vouchers(self):
                # $x('//section[contains(@*, "voucher")]//h3')
                card_voucers =  self.driver.find_elements(By.XPATH, r'//section[contains(@*, "voucher")]//h3')
                for voucher in card_voucers:
                    yield voucher.text


        def get_count_cards_deals(self):
            self.card_deals = self.driver.find_elements(By.XPATH,
                                                        r'//section[contains(@*, "deals")]/div[contains(@class, "base-cards")]')
            return len(self.card_deals)


        def get_image_deals(self):
            for deal in self.card_deals:
                try:
                    src = deal.find_element(By.XPATH, r'.//img').get_attribute('src')
                    self.cards_tray_image = [src, ]
                except:
                    src = 'Not found'
                    self.cards_tray_image = [src, ]
                yield src

        def scrolling_page(self, index):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", self.card_deals[index])
                time.sleep(0.6)
            except:
                pass

        def get_collect_deals(self):
                # $x('//section[contains(@*, "deals")]/div[contains(@class, "base-cards")]')
                self.card_deals =  self.driver.find_elements(By.XPATH, r'//section[contains(@*, "deals")]/div[contains(@class, "base-cards")]')
                for deal in self.card_deals:
                    yield deal.get_attribute('textContent')
                # yield self.card_deals[index].text

        def get_common_deals(self, index):
            yield self.card_deals[index].get_attribute('textContent')

        def get_image_deals_2(self):
            for deal in self.card_deals:
                try:
                    src = deal.find_element(By.XPATH, r'.//img').get_attribute('src')
                    self.image
                except:
                    src = ''
                yield src


        def get_collect_deals_2(self, index):
                # $x('//section[contains(@*, "deals")]/div[contains(@class, "base-cards")]')
                # for deal in self.card_deals[index]:
                #     yield self.card_deals[index].get_attribute('textContent')
                try:

                    try:
                        # image = self.driver.find_elements(By.XPATH,
                        #                                 rf'//section[contains(@*, "deals")]/div[contains(@class, "base-cards")][{index+1}]//img')
                        #
                        # # self.cards_tray_image = [self.card_deals[index].find_element(By.XPATH, r'.//img').get_attribute('src'), ]
                        # self.cards_tray_image = [image.get_attribute('src'), ]

                        image = self.driver.find_elements(By.XPATH,
                                                        rf'//section[@data-ref-id="deals-grid__section"]/div[{index+1}]//img')

                        # self.cards_tray_image = [self.card_deals[index].find_element(By.XPATH, r'.//img').get_attribute('src'), ]
                        self.cards_tray_image = [image.get_attribute('src'), ]
                    except:
                        self.cards_tray_image = ['Not found', ]
                    # yield self.card_deals[index].get_attribute('textContent')


                    card = self.driver.find_element(By.XPATH,
                                                      rf'(//section[@data-ref-id="deals-grid__section"]/div)[{index+1}]')
                    # card = self.driver.find_elements(By.XPATH,
                    #                                   rf'//section[contains(@*, "deals")]/div[contains(@class, "base-cards")][{index + 1}]')

                    yield card.get_attribute('textContent')



                except Exception as ex:
                    print(ex)
                    self.cards_tray_image = ['Not found', ]
                    yield 'Not found'
                # yield self.card_deals[index].text

        # $x('(//section[@data-ref-id="deals-grid__section"]/div)[2]//span[contains(text(), "Show")]')

        def get_button_collect_deals(self, index):
            xpath_set = (
                # r'.//span[contains(text(), "Show")]',
                # r'.//span[@class="base-button__text"]',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index + 1}]//div[@class="base-button__container"]/ancestor::button',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index + 1}]//span[contains(text(), "Show")]/ancestor::button',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index + 1}]//span[@class="base-button__text"]/ancestor::button',
            )
            for xpath in xpath_set:
                try:
                    button_element = self.driver.find_element(By.XPATH, xpath)
                    button_element.click()
                    print(f'button click {index} {xpath}')
                    break
                except:
                    print(f'button click {index} {xpath} error')
                    continue
            time.sleep(0.5)
            try:
                # $x('//section//div[@data-ref-id="base-cards-tray__container"]//section[@data-ref-id="base-grid"]//div[@class="base-deal-card"]')
                cards_tray = self.driver.find_elements(By.XPATH,'//section//div[@data-ref-id="base-cards-tray__container"]//section[@data-ref-id="base-grid"]//div[@class="base-deal-card"]')
                cards_tray_content = [i.get_attribute('textContent') for i in cards_tray]
                # print(cards_tray)
            except:
                # print('tray card error')
                cards_tray_content = ['',]

            try:
                self.cards_tray_image = [i.find_element(By.XPATH, r'.//img').get_attribute('src') for i in cards_tray]
                if self.cards_tray_image:
                    raise
                # print(cards_tray_image)
            except:
                self.cards_tray_image = ['Not found',]

            for card in cards_tray_content:
                yield card




        def get_count_cards_deals_2(self):
            self.card_deals = self.driver.find_elements(By.XPATH,
                                                        r'//section[@data-ref-id="deals-grid__section"]/div')
            return len(self.card_deals)

        def is_type_button(self, index):
            # class="base-button__container"
            xpath_collections = (
                # r'.//span[contains(text(), "Show")]',
                # r'.//span[@class="base-button__text"]',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index+1}]//div[@class="base-button__container"]',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index+1}]//span[contains(text(), "Show")]',
                rf'//section[@data-ref-id="deals-grid__section"]/div[{index+1}]//span[@class="base-button__text"]',
            )
            for xpath in xpath_collections:
                try:
                    time.sleep(0.5)
                    # button_element =  self.card_deals[index].find_element(By.XPATH, xpath)
                    button_element = self.driver.find_element(By.XPATH, xpath)
                    # print(button_element)
                    return button_element
                except Exception as ex:
                    # print(ex)
                    continue
            else:
                return False


        def get_type_card(self, index):

            button_type = bool(self.is_type_button(index))
            type_card = {
                True: 'common_type',
                button_type: 'button_type',
            }
            # print(f'type_card: {type_card[True]}')
            return type_card[True]

        def get_cards_tray_image(self):
            for image in self.cards_tray_image:
                yield image