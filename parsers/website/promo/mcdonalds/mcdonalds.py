import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd

from database.database import DataBase
import setting

def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
        time.sleep(1)
    except:
        pass




def run_browser():

    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])


    url = 'https://www.mcdonalds.com/gb/en-gb/deals.html'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver






def parse():

    driver = run_browser()

    click_accept(driver)



    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []
    time.sleep(3333)
    # deals 1
    head = [i.text for i in driver.find_elements(By.XPATH, '//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//h2')]
    text = [i.text for i in driver.find_elements(By.XPATH, '//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//p')]
    image = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//div[contains(@class, "desktop")]//img[contains(@src, "Desktop")]')]

    print(head)
    print(text)
    print(image)
    print('====================')
    for h, t, i in zip(head, text, image):
        data.append([date, city,post_code,h, t, i])

    # deals 2
    head = [i.text for i in driver.find_elements(By.XPATH,
                                '//div[@class="featurecallout"]//h2')]
    text = [i.text for i in driver.find_elements(By.XPATH,
                                '//div[@class="featurecallout"]//div[@class="head-desc-container"]//div/span')]
    image = [i.get_attribute('src') for i in driver.find_elements(By.XPATH,
                                '//div[@class="featurecallout"]//div//img')]

    print(head)
    print(text)
    print(image)
    print('====================')
    for h, t, i in zip(head, text, image):
        data.append([date, city,post_code,h, t, i])


    columns = {
        0: 'date',
        1: 'post_code',
        2: 'city',
        3: 'head',
        4: 'text',
        5: 'image',
    }
    data = pd.DataFrame(data)
    data_frame = data.rename(columns=columns)
    # data.to_excel(f"mcdonalds_{str(date)}.xlsx")
    print(data_frame)
    # DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_JUST_EATS_PROMO')
def start_mcdonalds_promo():
    parse()


# $x('//div[contains(@class, "container responsivegrid")]/div/div[contains(@class, "aem-Grid")]/div[contains(@class, "columnlayout")]')

class McDonaldsPromoParser():

    def __init__(self):
        self.url = 'https://www.mcdonalds.com/gb/en-gb/deals.html'
        self.driver = self.run_browser()
        self.cards = self.get_cards_deals()
        self.parse()
        self.driver.close()
        self.driver.quit()

    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        path = setting.SELENIUM['path']
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])

        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        time.sleep(2)
        driver.get(url=self.url)
        time.sleep(5)
        return driver

    def get_cards_deals(self):
        xpath = r'//div[contains(@class, "container responsivegrid")]/div/div[contains(@class, "aem-Grid")]/div[contains(@class, "columnlayout")]'

        return self.driver.find_elements(By.XPATH, xpath)

    def get_image(self, card):
        try:
            return card.find_element(By.XPATH, r'.//img').get_attribute('src')
        except:
            return 'Not found'

    def get_head(self, card):
        try:
            return card.find_element(By.XPATH, r'.//h2').text
        except:
            return 'Not found'

    def get_description(self, card):
        try:
            return card.find_element(By.XPATH, r'.//div[contains(@class, "cmp-teaser__description")]').text
        except:
            return 'Not found'

    def parse(self):
        date = datetime.now().strftime("%d.%m.%Y")
        for card in self.cards:
            image_url = self.get_image(card)
            item_name = self.get_head(card)
            description = self.get_description(card)
            print(image_url)
            print(item_name)
            print(description)
            data = pd.DataFrame({
                'date':date,
                'source':self.url,
                'postcode':'',
                'item':item_name,
                'description':description,
                'image':image_url,
            }, index=[0])
            self.to_stg_db(data)


    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_mcdonald_promo')