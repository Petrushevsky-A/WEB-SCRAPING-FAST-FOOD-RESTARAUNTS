
    #https://www.mcdonalds.com/gb/en-gb/deals.html

    # deals 1
    # h2
    #'//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//h2'

    # p
    # '//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//p'

    # img
    #'//div[@class = "columncontrol parbase"]//div[contains(@class, "isDesktop")]//div[contains(@class, "desktop")]//img[contains(@src, "Desktop")]'

    # deals 2
    # h2
    # '//div[@class="featurecallout"]//h2'

    # span
    # '//div[@class="featurecallout"]//div[@class="head-desc-container"]//div/span'

    # img
    # '//div[@class="featurecallout"]//div//img'


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

    url = 'https://www.mcdonalds.com/gb/en-gb/deals.html'
    path = r'chromedriver.exe'
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
    time.sleep(3)
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
    data = data.rename(columns=columns)
    data.to_excel(f"mcdonalds_{str(date)}.xlsx")

if __name__ == '__main__':
    parse()
