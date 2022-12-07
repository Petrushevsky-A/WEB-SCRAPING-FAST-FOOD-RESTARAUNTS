
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import pandas as pd
import requests

import time
from datetime import datetime

from database.database import DataBase

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)


url = 'https://www.nandos.co.uk/food/menu/'

driver.get(url = url)
time.sleep(5)
try:
    driver.find_element(By.XPATH, '//button[@id="truste-consent-button"]').click()
    time.sleep(1)
except:
    pass
sidebar = [1]

nutrtion_informations = []

for side in sidebar:

    time.sleep(1)

    list_category_selenium_elements = []
    list_foods_selenium_elements = []

    for id, val in enumerate(driver.find_elements(By.XPATH, '//section')):
        category = driver.find_element(By.XPATH, f'//*/section[{id + 1}]/h2[1]/em[1]').text
        elements = driver.find_elements(By.XPATH, f'//*/section[{id+1}]//button[contains(@title, "Open product")]')
        list_foods_selenium_elements.append(elements)
        list_category_selenium_elements.append([category for x in elements])

    list_foods_selenium_elements = sum(list_foods_selenium_elements, [])
    list_category_selenium_elements = sum(list_category_selenium_elements, [])
    print(list_foods_selenium_elements)
    print(list_category_selenium_elements)

    #

    for food, category_food in zip(list_foods_selenium_elements, list_category_selenium_elements):
        print(f'category_food: {category_food}')

        driver.execute_script("arguments[0].click();", food)
        # food.click()

        time.sleep(3)
        name = driver.find_element(By.XPATH, '//div[@class="inner"]/h3').text
        print(name)

        driver.find_element(By.XPATH, '//div[@class="tabs"]/ul/li[2]').click()
        time.sleep(1)

        category_nutrtion_information = []
        value_nutrtion_information = []

        try:
            category_nutrtion_information = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@id, "react-tabs")]/div/table/tbody/tr/th[1]')]
            value_nutrtion_information = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@id, "react-tabs")]/div/table/tbody/tr/th[2]')]
        except:
            print(f"ERROR {name}")

        print(name)


        print(category_nutrtion_information)
        print(value_nutrtion_information)


        time.sleep(2)


        # Забрать ценник
        price = "empty"
        try:
            price = driver.find_element(By.XPATH, '//div[contains(@class, "inner")]/div[contains(@class, "price")]').text
        except:
            print(f'ERROR PRICE')

        list_img_file = []
        list_img_src = []

        src_img = driver.find_element(By.XPATH, '//div[@class="hero"]/img').get_attribute("src")

        print(src_img)
        directory = "nandos_img"
        name_img = name
        try:
            reponse_img = requests.get(src_img)
            if reponse_img.status_code == 200:
                with open(f"./{directory}/{name_img}.jpg", "wb") as file:
                    file.write(reponse_img.content)
        except:
            print(f"ERROR {src_img}")
        ingridient = "empty"
        try:
            ingridient = ", ".join([i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//div[contains(@class, "panel")]/p')])
        except:
            print(f"ERROR: {ingridient}")

        description = 'Not found'
        try:
            description = driver.find_element(By.XPATH, '//div[contains(@class, "inner")]/p').text
        except:
            description = 'Not found'

        print(f'ingridient: {description}')
        driver.find_element(By.XPATH, '//a[@class="close"]').click()
        time.sleep(2)

        nutrtion_informations.append([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, "empty", ingridient, price, description])
        print([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, "empty", ingridient, price, description])
        time.sleep(1)

category = {}
for nutrtion_information in nutrtion_informations:
    for i in nutrtion_information[3]:
        print(i)
        category[i] = None

category = [i for i in category]

data_nutrtion_informations = {}
for i in category:
    data_nutrtion_informations[i] = []

date = datetime.now().strftime("%d.%m.%Y")
data_nutrtion_informations['date'] = []
data_nutrtion_informations['names'] = []
data_nutrtion_informations['img_src'] = []
data_nutrtion_informations['img_directory_file'] = []
data_nutrtion_informations['category_food'] = []
data_nutrtion_informations['size'] = []
data_nutrtion_informations['ingridient'] = []
data_nutrtion_informations['price_food'] = []
data_nutrtion_informations['description'] = []
for nutrtion_information in nutrtion_informations:
    data_nutrtion_informations['date'].append(date)
    data_nutrtion_informations['names'].append(nutrtion_information[0])
    data_nutrtion_informations['img_src'].append(nutrtion_information[1])
    data_nutrtion_informations['img_directory_file'].append(nutrtion_information[2])
    data_nutrtion_informations['category_food'].append(nutrtion_information[5])
    data_nutrtion_informations['size'].append(nutrtion_information[6])
    data_nutrtion_informations['ingridient'].append(nutrtion_information[7])
    data_nutrtion_informations['price_food'].append(nutrtion_information[8])
    data_nutrtion_informations['description'].append(nutrtion_information[9])
    for cat, val in zip(nutrtion_information[3],nutrtion_information[4]):
        data_nutrtion_informations[cat].append(val)
    for i in category:
        if not(i in nutrtion_information[3]):
            data_nutrtion_informations[i].append('Empty')

driver.close()
driver.quit()

DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_DELIVEROO_PRICE')