import time
import itertools

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
import numpy as np
from database.database import DataBase

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



def start_uber_eats_promo():
        path = r'chromedriver.exe'
        post_codes = [
                # 'W1C 1LX',
                # 'CF10 1PN',
                # 'BT1 5AA',
                # 'G1 3SQ',#1
                # 'B2 4QA',
                # 'L1 8JQ',
                # 'LS1 1UR',
                'M2 5DB',
                ]
        cities = [
                # 'London',
                # 'Cardiff',
                # 'Belfast',
                # 'Glasgow',
                # 'Birmingham',
                # 'Liverpool',
                # 'Leeds',
                'Manchester'
            ]

        url = 'https://www.ubereats.com/gb'



        for post_code, city in zip(post_codes, cities):


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


                DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_UBER_EATS_PROMO')

                driver.close()
                driver.quit()



