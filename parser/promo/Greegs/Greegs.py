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


def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(1)
    except:
        pass




def run_browser():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    url = 'https://www.greggs.co.uk/news'
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver






def parse():

    driver = run_browser()

    click_accept(driver)
    # https://www.greggs.co.uk/news


    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []
    # $x('//button[contains(text(), "more")]')
    driver.find_element(By.XPATH, '//button[contains(text(), "more")]').click()
    time.sleep(1)

    # $x('//article[@class="container"]')

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
    data = data.rename(columns=columns)
    data.to_excel(f"greegs_{str(date)}.xlsx")

if __name__ == '__main__':
    parse()
