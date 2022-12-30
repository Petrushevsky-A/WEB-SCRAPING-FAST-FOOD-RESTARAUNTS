from datetime import datetime
from time import sleep

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

from database.database import DataBase
import setting

def promo_position(title, description, picture):
    promo = {
        'start_date': datetime.now().strftime("%d.%m.%Y"),
        'end_date': '',
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
    return promo


class Parse:
    def __init__(self):
        self.data = list()
        self.driver = self.configuring_driver()

    def parse(self):

        DEALS = [i.get_attribute('innerHTML') for i in self.driver.find_elements(By.XPATH, '//main/div')]
        print(len(DEALS))
        for i in range(0, len(DEALS), 3):
            try:
                try:
                    image_url = [self.driver.find_element(By.XPATH, f'//main/div[{i + 2}]//img').get_attribute('src')]
                except:
                    try:
                        image_url = [i.get_attribute('src') for i in
                                     self.driver.find_elements(By.XPATH, f'//main/div[{i + 3}]//img')]
                    except:
                        image_url = ''

                html_text_deal = etree.HTML(DEALS[i + 2])
                title_deal = [i.text for i in html_text_deal.xpath('//h2')]
                text_deal = [i.text for i in html_text_deal.xpath('//strong')]
                if len(text_deal) == 0:
                    text_deal = [i.text for i in html_text_deal.xpath('//p')]

                for deal in range(len(title_deal)):
                    self.data.append(promo_position(title_deal[deal], text_deal[deal], image_url[deal]))

            except Exception as ex:
                print(ex)

    def __call__(self, *args, **kwargs):
        self.driver.get(url='https://www.kfc.co.uk/kfc-deals')
        sleep(3)

        self.parse()

        self.driver.close()
        self.driver.quit()

        data = sum(self.data, [])
        data_frame = pd.DataFrame(data)
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_kfc_promo')


    def configuring_driver(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)

        return driver


def start_kfc_promo():
    Parse()()
