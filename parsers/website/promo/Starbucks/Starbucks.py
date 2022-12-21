


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
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    url = 'https://www.starbucks.co.uk/rewards'
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
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