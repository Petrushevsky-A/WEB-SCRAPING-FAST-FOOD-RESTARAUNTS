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
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    url = 'https://www.kfc.co.uk/kfc-deals'
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    return driver






def parse():

    driver = run_browser()

    click_accept(driver)
    # https://www.kfc.co.uk/kfc-deals

    #deals 1
    city = "London"
    post_code = "W1C 1LX"
    date = datetime.now().strftime("%d.%m.%Y")
    data = []
    head = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@class, "q98cj5")]//h2')]
    text = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@class, "q98cj5")]//div[p]')]
    image = [i.value_of_css_property('background-image')[5:-2] for i in driver.find_elements(By.XPATH, '//div[contains(@class, "q98cj5")]/div[1]')]
    print(head)
    print(text)
    print(image)
    for h, t, i in zip(head, text, image):
        data.append([date, city,post_code,h, t, i])
    # deals 2

    button = driver.find_element(By.XPATH, '//a[button[@label="VIEW DEAL"]]')
    driver.execute_script("arguments[0].click();", button)
    # logo
    time.sleep(3)

    image = [driver.find_element(By.XPATH, '//li[@class="slide selected"]//img').get_attribute('src')]
    head =[ driver.find_element(By.XPATH, '//div//h2').text]
    text = [driver.find_element(By.XPATH, '//main/div[2]').text]

    print(f'image {image}')
    print(f'head {head}')
    print(f'text {text}')
    for h,t,i in zip(head,text,image):
        data.append([date, city,post_code,h, t, i])

    image = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//main/div[3]//img')]
    head = [i.text for i in driver.find_elements(By.XPATH, '//main/div[3]//h2')]
    text = ['Not found' for i in head]

    print(image)
    print(head)
    print(text)
    for h, t, i in zip(head, text, image):
        data.append([date, city,post_code,h, t, i])
    print('=========')
    print(data)
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
    data.to_excel(f"kfc_{str(date)}.xlsx")

if __name__ == '__main__':
    parse()
