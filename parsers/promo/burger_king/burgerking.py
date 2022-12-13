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


def click_accept(driver):
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
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

    url = 'https://www.burgerking.co.uk/rewards/offers'
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver






def start_burgerking_promo():

    driver = run_browser()

    click_accept(driver)
    # https://www.burgerking.co.uk/rewards/offers


    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []

    list_cards_deals = driver.find_elements(By.XPATH, '//div[@data-testid="browsing-panel"]//li')
    for id, val in enumerate(list_cards_deals[:-1], 1):

        driver.execute_script("arguments[0].scrollIntoView();", val)
        time.sleep(0.1)
        head = "".join([i.text for i in driver.find_elements(By.XPATH, f'//div[@data-testid="browsing-panel"]//li[{id}]//h3')])
        text = "".join([i.text for i in driver.find_elements(By.XPATH, f'//div[@data-testid="browsing-panel"]//li[{id}]//p')])
        try:
            image = [i.get_attribute('srcset').split(',')[0][:-4] for i in driver.find_elements(By.XPATH, f'//div[@data-testid="browsing-panel"]//li[{id}]//div[picture][2]//source')][0]
        except:
            image = 'Not found'
        print(head)
        print(text)
        print(image)
        print('====================')
        data.append([date,post_code,city,head,text,image])

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
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_BURGER_KING_PROMO')
