
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import pandas as pd

from database.database import DataBase
import time

import setting

def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(1)
    except:
        pass




def run_browser():
    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
    url = 'https://www.greggs.co.uk/news'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver






def start_greegs_promo():

    driver = run_browser()

    click_accept(driver)


    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []

    driver.find_element(By.XPATH, '//button[contains(text(), "more")]').click()
    time.sleep(1)


    list_cards_deals = driver.find_elements(By.XPATH, '//article[@class="container"]')

    images = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, f'//article[@class="container"]//img')]
    texts = [i.text for i in driver.find_elements(By.XPATH, f'//article[@class="container"]//p')]
    heads = [i.text for i in driver.find_elements(By.XPATH, f'//article[@class="container"]//h2')]
    print(heads)
    print(texts)
    print(images)
    print('====================')
    for h,t,i in zip(heads, texts, images):
        data.append([date,post_code,city,h,t,i])

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

    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_GREEGS_PROMO')

