from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

from database.database import DataBase
import setting

def get_product(category, name, price, picture):
    product = {
        'Start date': [datetime.now().strftime("%d.%m.%Y")],
        'End date': [datetime.now().strftime("%d.%m.%Y")],
        'Brand': ["Nando's"],
        'Address': [''],
        'City': [''],
        'Postcode': [''],
        'Segment': [''],
        'Category': [category],
        'Category 2': [''],
        'Category 3': [''],
        'Category 4': [''],
        'Item': [name],
        'Source': ['https://www.nandos.co.uk/'],
        'Region': ['UK'],
        'Price(£)': [price],
        'Status': ['on'],
        'Picture': [picture],
    }
    return product


class Parse():
    def __init__(self, driver):
        self.data = []
        self.driver = driver

    def get_name(self):
        try:
            name = self.driver.find_element(By.XPATH, '//div[@class="inner"]//h3').get_attribute('innerHTML')
        except:
            name = 'Not found'
        return name

    def get_image_url(self):
        try:
            image_url = self.driver.find_element(By.XPATH, '//div[@class="inner"]//img').get_attribute('src')
        except:
            image_url = 'Not found'
        return image_url

    def get_position(self, category):
        try:
            size = {
                'name': [f'{self.get_name()} {i.get_attribute("innerHTML")}' for i in self.driver.find_elements(By.XPATH, '//table//tr/th')],
                'price': [i.get_attribute('innerHTML')[1:] for i in self.driver.find_elements(By.XPATH, '//table//tr/td')]
            }

            if len(size['name']):
                for i in range(len(size['name'])):
                    self.data.append(get_product(category, size['name'][i], size['price'][i], self.get_image_url()))
            else:
                price = self.driver.find_element(By.XPATH, '//div[@class="inner"]//div[@class="price"]').get_attribute(
                    'innerHTML')[1:]
                name = self.get_name()
                self.data.append(get_product(category, name, price, self.get_image_url()))

        except:
            print(f'ERROR: {category}')

    def get_category(self, buttons, category):
        for button in buttons:
            try:
                k = 1
                while k:
                    try:

                        button.click()
                        sleep(1)
                        self.get_position(category)
                        k = 0
                    except:
                        self.driver.execute_script(f'window.scrollBy(0, {100});')
                        sleep(0.2)

            except:
                pass

    def get_nandinos_kids(self, divs, category):
        subSection = ''
        sets = dict()
        for div in divs:
            k = 1
            while k:
                if div.get_attribute('class') == 'subSection':
                    subSection = div.get_attribute('innerHTML')
                    sets[subSection] = list()
                    k = 0

                else:
                    try:
                        div.click()
                        sleep(1)
                        name = self.driver.find_element(By.XPATH, '//div[@class="inner"]//h3').get_attribute('innerHTML')
                        sets[subSection].append(name)
                        self.driver.find_element(By.XPATH, '//a[@class="close"]').click()
                        k = 0
                    except:
                        self.driver.execute_script(f'window.scrollBy(0, {100});')
                        sleep(0.2)

        for mains in sets['Mains']:
            for sides in sets['Nandino sides']:
                for ireland in sets['Available in Northern Ireland']:
                    for drink in sets['Dessert OR Drink']:
                        self.data.append(get_product(category, f'{mains}, {sides}, {ireland}, {drink}', '5.95', 'Not found'))

    def __call__(self, *args, **kwargs):
        id_sections = [i.get_attribute('id') for i in self.driver.find_elements(By.XPATH, '//section')]
        for id in id_sections:
            category = self.driver.find_element(By.XPATH, f'//section[@id="{id}"]/h2').get_attribute('innerHTML')
            if id == 'section_nandinos-kids':
                divs = self.driver.find_elements(By.XPATH, f'//section[@id="section_nandinos-kids"]/div[2]/*')
                self.get_nandinos_kids(divs, category)
            else:
                buttons = self.driver.find_elements(By.XPATH, f'//section[@id="{id}"]//button')
                self.get_category(buttons, category)
        return self.data


def start():
    driver = configuring_driver()

    driver.get(url='https://www.nandos.co.uk/food/menu/')
    sleep(3)
    driver.find_element(By.XPATH, '//button[@id="truste-consent-required"]').click()
    sleep(1)
    data = list()

    data.append(Parse(driver=driver)())

    driver.close()
    driver.quit()

    print(data)
    data_frame = pd.DataFrame(data)

    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_nandos_price')

def configuring_driver():
    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    # options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    return driver

def start_nandos_price():
    start()
