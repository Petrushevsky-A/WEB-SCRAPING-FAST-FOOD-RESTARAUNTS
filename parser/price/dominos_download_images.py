
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

files = [i for i in os.listdir('.') if '.xlsx' in i and 'dominos_price' in i]
print(files)
print(len(files))

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
for file in files:
    pd_data = pd.read_excel(f'{file}')

    for pd_i in zip(pd_data['Item'],pd_data['Picture']):
        src_img = pd_i[1]
        src_img = src_img[:src_img.find("?")]
        directory = "dominos_img"
        name_img = pd_i[0].strip()




        driver.get(url=src_img)
        time.sleep(2)


        driver.find_element(By.XPATH, '//img').screenshot(f"{directory}/{name_img}.jpg")
        # try:
        #
        #     reponse_img = requests.get(f"{src_img}")
        #     print(reponse_img.content)
        #     print(src_img)
        #     break
        #     if reponse_img.status_code == 200:
        #         with open(f"{directory}/{name_img}.jpg", "wb") as file:
        #             file.write(reponse_img.content)
        #             print(f"TRUE {src_img}")
        #
        # except Exception as ex:
        #     print(ex)
        #     print(f"ERROR {src_img}")
