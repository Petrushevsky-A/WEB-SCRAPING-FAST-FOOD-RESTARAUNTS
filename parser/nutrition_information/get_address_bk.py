import time
from datetime import datetime

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)



def get_one_level_links_li_elements(driver):
    try:
        return [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//a[contains(@class, "listLink")]')]
    except:
        return []


def get_two_level_links_li_elements(driver):
    try:
        list_url = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//li[contains(@class, "listTeaser")]/*/a')]
        if not list_url:
            list_url = driver.current_ur
        return list_url
    except:
        return [driver.current_url]

def run_url(url, driver=driver):
    try:
        driver.get(url=url)
        time.sleep(2)
        level_two_links = get_two_level_links_li_elements(driver)
        print(level_two_links)
        return level_two_links
    except:
        return [url]

def get_links_restaurant():
    url= 'https://locations.burgerking.co.uk/'
    # url= 'https://locations.burgerking.co.uk/coatbridge/unit2-caldeen-road'
    # url = 'https://locations.burgerking.co.uk/ipswich'

    driver.get(url=url)
    time.sleep(5)

    level_one_links = get_one_level_links_li_elements(driver)
    level_two_links = list(map(run_url, level_one_links))

    level_two_links = sum(level_two_links, [])
    level_two_links = pd.DataFrame({'urls': level_two_links})

    date = datetime.now().strftime("%d.%m.%Y")
    level_two_links.to_excel(f'bk_adress_restaurants_{str(date)}.xlsx')
    print('==========final result==========')
    print(level_two_links)


get_links_restaurant()
driver.close()
driver.quit()