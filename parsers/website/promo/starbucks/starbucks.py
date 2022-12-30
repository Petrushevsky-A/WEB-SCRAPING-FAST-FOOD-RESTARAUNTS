


import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd

import numpy as np

from multiprocessing import Pool
from lxml import etree

from database.database import DataBase
import setting


# Подтверждение в модальном окне
def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(1)
    except:
        pass



# Запуск браузера
def run_browser():
    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    url = 'https://www.starbucks.co.uk/rewards'
    driver.get(url=url)
    time.sleep(5)
    return driver






def start_startuck_promo():

    driver = run_browser()

    click_accept(driver)


    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []
    # $x('//button[contains(text(), "more")]')

    # $x('//article[@class="container"]')

    list_cards_deals = driver.find_elements(By.XPATH, '//article[@class="container"]')

    # $x('(//section)[3]//div[@class = "content"]//h2').map( i=> i.textContent )
    # $x('//ul[contains(@class, "items")]/li').map( i=> i.textContent )

    # $x('(//section)[4]//div[@class = "content"]//h2').map( i=> i.textContent )
    # $x('(//section)[4]//div[@class = "content"]//div[contains(@class, "rich-text")]').map( i=> i.textContent )

    texts = [i.text for i in driver.find_elements(By.XPATH, f'//ul[contains(@class, "items")]/li')]
    heads = driver.find_element(By.XPATH, f'(//section)[3]//div[@class = "content"]//h2').text
    heads = [heads for i in texts]
    print(heads)
    print(texts)

    print('====================')
    for h,t in zip(heads, texts):
        data.append([date,post_code,city,h,t])

    texts = [i.text for i in driver.find_elements(By.XPATH, f'(//section)[4]//div[@class = "content"]//div[contains(@class, "rich-text")]')]
    heads = driver.find_element(By.XPATH, f'(//section)[4]//div[@class = "content"]//h2').text
    heads = [heads for i in texts]
    print(heads)
    print(texts)

    print('====================')
    for h, t in zip(heads, texts):
        data.append([date, post_code, city, h, t])

    columns = {
        0: 'date',
        1: 'post_code',
        2: 'city',
        3: 'head',
        4: 'text',

    }
    data = pd.DataFrame(data)
    data_frame = data.rename(columns=columns)
    # data.to_excel(f"sturbacks_{str(date)}.xlsx")

    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_STARBUCKS_PROMO')