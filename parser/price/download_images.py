
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


import pandas as pd
import requests
import numpy as np
from multiprocessing import Pool
from lxml import etree
import os

from urllib.request import Request, urlopen

files = ['Недостающие картинки (1).xlsx', ]
print(files)
print(len(files))

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
for file in files:
    pd_data = pd.read_excel(f'{file}')

    for index, url in zip(pd_data['item'],pd_data['url']):
        try:
            print(index)
            print(url)
            directory = "новые_img"





            driver.get(url=url)
            time.sleep(2)


            driver.find_element(By.XPATH, '//img').screenshot(f"{directory}/{index}.png")
        except:
            continue
