from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

from database.database import DataBase


def promo_position(title, description, picture):
    promo = {
        'start_date': datetime.now().strftime("%d.%m.%Y"),
        'end_date': datetime.now().strftime("%d.%m.%Y"),
        'brand': 'KFC',
        'segment': '',
        'city': '',
        'postcode': '',
        'title': title,
        'promo_description_1_8': description,
        'promo_type': '',
        'promo_type_edited': '',
        'app_in_store': '',
        'promo_title_edited': '',
        'product_category': '',
        'product_category_edited': '',
        'source': 'kfc.co.uk',
        'source_type': 'Website',
        'region': 'UK',
        'picture': picture,
    }
    print(promo)

    data_frame = pd.DataFrame(promo, index=[0])
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_kfc_promo')

    return promo


class Parse:
    def __init__(self):
        self.data = list()
        self.driver = configuring_driver()

    def parse(self):

        DEALS = self.driver.find_elements(By.XPATH, '//main/div')

        for i in range(1, len(DEALS) + 1):

            try:
                picture = self.driver.find_element(By.XPATH, f'//main/div[{i}]//ul[@class="slider animated"]/li[2]/div').get_attribute('src')
                title = self.driver.find_element(By.XPATH, f'//main/div[{i+1}]//h2').get_attribute('innerHTML').replace('<br>', '').replace('&nbsp;', '').replace('\n', ' ').replace('amp;', '')
                description = self.driver.find_element(By.XPATH, f'//main/div[{i+1}]//strong').get_attribute('innerHTML').replace('<br>', '').replace('&nbsp;', '').replace('\n', ' ').replace('amp;', '')

                self.data.append(promo_position(title, description, picture))
            except:
                try:
                    pictures = [i.get_attribute('src') for i in self.driver.find_elements(By.XPATH, f'//main/div[{i}]//img')]
                    titles = [i.get_attribute('innerHTML').replace('<br>', '').replace('&nbsp;', '').replace('\n', ' ').replace('amp;', '') for i in self.driver.find_elements(By.XPATH, f'//main/div[{i}]//h2')]
                    descriptions = [i.get_attribute('innerHTML').replace('<br>', '').replace('&nbsp;', '').replace('\n', ' ').replace('amp;', '') for i in self.driver.find_elements(By.XPATH, f'//main/div[{i}]//p')]

                    for j in range(len(pictures)):
                        self.data.append(promo_position(titles[j], descriptions[j], pictures[j]))
                except:
                    pass

    def __call__(self, *args, **kwargs):
        self.driver.get(url='https://www.kfc.co.uk/kfc-deals')
        sleep(3)

        self.parse()

        self.driver.close()
        self.driver.quit()



def configuring_driver():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.99 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    return driver


def start_kfc_promo():
    Parse()()

