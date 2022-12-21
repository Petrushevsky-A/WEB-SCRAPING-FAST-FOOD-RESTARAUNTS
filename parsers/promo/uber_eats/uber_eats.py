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
                while True:
                        try:
                                self.driver.find_element(By.XPATH, '//button[text() = "Show more"]').click()
                                time.sleep(4)
                        except:
                                break
                self.cards = self.driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div')
                for element in self.cards:
                        self.driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(0.15)

        # get html
        # get image
        # get alt image
        # get head
        # get alt head
        # get description
        # get alt description
        # get prices
        # get alt prices
        # get times
        # get alt times
        # get rating
        # get alt rating

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

        def get_alt_image(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_head(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/h3').get_attribute('src')
                except:
                        return 'Not Found'

        def get_alt_head(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_description(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_alt_description(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_prices(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_alt_prices(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_times(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_alt_times(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_rating(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'

        def get_alt_rating(self, index):
                try:
                        return self.cards[index].find_element(By.XPATH, './/img').get_attribute('src')
                except:
                        return 'Not Found'


def start_promo_uber_eats():
        path = r'chromedriver.exe'
        post_codes = [
                'W1C 1LX',
                'CF10 1PN',
                'BT1 5AA',
                'G1 3SQ',#1
                'B2 4QA',
                'L1 8JQ',
                'LS1 1UR',
                'M2 5DB',
                ]
        citys = [
                'London',
                'Cardiff',
                'Belfast',
                'Glasgow',
                'Birmingham',
                'Liverpool',
                'Leeds',
                'Manchester'
            ]

        url = 'https://www.ubereats.com/gb'



        for post_code, city in zip(post_codes, citys):


                driver = webdriver.Chrome(chrome_options=options, executable_path=path)
                time.sleep(2)
                driver.get(url=url)
                time.sleep(5)
                try:
                        driver.find_element(By.XPATH, '//div[@id="cookie-banner"]//button[text() = "Accept"]').click()
                        time.sleep(1)
                except:
                        pass
                # set input
                driver.find_element(By.XPATH, '//input[@name="searchTerm"]').send_keys(f'{post_code}')
                time.sleep(1)
                driver.find_element(By.XPATH, '//input[@name="searchTerm"]').send_keys(Keys.ENTER)
                time.sleep(8)

                # filter
                try:
                        driver.find_element(By.XPATH,
                                            '//div[contains(@class,"aw")]/parent::div/preceding-sibling::div//div[text() = "Deals"]').click()
                        time.sleep(5)
                except:
                        pass

                # нужно отлистать весь лист чтобы подгрузились все данные
                # нажимает еще пока не подгрузяться все таблички

                while True:
                        try:
                                driver.find_element(By.XPATH, '//button[text() = "Show more"]').click()
                                time.sleep(4)
                        except:
                                break

                for element in driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div'):
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(0.15)




                names = [i.text for i in driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div//h3')]
                print(names)

                descriptions = [i.text for i in driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div/div/div[1]/div[1]/div[1]/div[2]')]
                print(descriptions)


                link_images = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//div[@class="lazyload-wrapper "]/picture/img')]
                # directorys = []
                # for name, link_image in zip(names, link_images):
                #         time.sleep(1)
                #         directory = f"./uber_eats/{name}.jpeg"
                #         try:
                #                 reponse_img = requests.get(link_image)
                #                 if reponse_img.status_code == 200:
                #                         with open(directory, "wb") as file:
                #                                 file.write(reponse_img.content)
                #                         directorys.append(directory)
                #         except:
                #                 print(f"ERROR {link_image}")
                #                 directorys.append('Not found')

                prices = [i.text for i in driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/span')]
                times = [i.text for i in driver.find_elements(By.XPATH, '//div[@data-test="feed-desktop"]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/span')]
                print(prices)
                print(times)
                curent_url = driver.current_url
                pc = [post_code for i in names]
                city = [city for i in names]
                date = datetime.now().strftime("%d.%m.%Y")
                date = [date for i in names]
                data = list(itertools.zip_longest(date, pc, city,names,descriptions,prices,times, link_images, fillvalue = ''))
                columns = {
                        0: 'dates',
                        1: 'post_code',
                        2: 'city',
                        3: 'names',
                        4: 'descriptions',
                        5: 'prices',
                        6: 'times',
                        7: 'link_images',
                }
                print(data)
                data_frame = pd.DataFrame(data)

                data_frame = data_frame.rename(columns=columns)
                date = datetime.now().strftime("%d.%m.%Y")


                DataBase().to_stg_table(data_frame=data_frame, name_stg_table='promo_uber_eats')

                driver.close()
                driver.quit()



