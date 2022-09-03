import time
from datetime import datetime

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
date = datetime.now().strftime("%d.%m.%Y")
urls = pd.read_excel(f"mcdonalds_url_foods_{str(date)}.xlsx")["links"]
category = pd.read_excel(f"mcdonalds_url_foods_{str(date)}.xlsx")["category"]



nutrtion_informations = []

for url, category_food in zip(urls, category):
    try:
        driver.get(url=url)
        time.sleep(5)

        name = driver.find_element(By.XPATH, '//h1[contains(@class, "heading")]').text
        print(name)


        category_nutrtion_information = []
        value_nutrtion_information = []

        try:
            category_nutrtion_information = ["".join([i.get_attribute('innerHTML'),j.get_attribute('innerHTML')]) for i, j in zip(driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-table")]/table/tbody/tr/th[1]/span[1]'),driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-table")]/table/tbody/tr/th[1]/span[2]'))]
            temp = [driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-table")]/table/tbody/tr/th[2]/span[1]'), driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-table")]/table/tbody/tr/td[1]/span[1]')]
            temp =sum(temp, [])
            value_nutrtion_information = [i.get_attribute('innerHTML').strip() for i in temp]
        except:
            print(f"ERROR {name}")




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

        src_img = 'https://www.mcdonalds.com/' + driver.find_element(By.XPATH, '//img[contains(@class, "img-responsive")]').get_attribute("srcset")

        print(src_img)
        directory = "mcdonalds_img"
        name_img = name
        try:
            reponse_img = requests.get(src_img)
            if reponse_img.status_code == 200:
                with open(f"./{directory}/{name_img}.png", "wb") as file:
                    file.write(reponse_img.content)
        except:
            print(f"ERROR {src_img}")
        ingridient = "empty"
        try:
            ingridient = "".join([i.text for i in driver.find_elements(By.XPATH, '//p[contains(@class,  "description")]')])
        except:
            pass
            # try:
            #     ingridient = ", ".join([i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//div[contains(@class, "panel")]/p')])
            # except:
            #     print(f"ERROR: {ingridient}")

        print(f'ingridient: {ingridient}')


        nutrtion_informations.append([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, "empty", ingridient, price])
        print([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, "empty", ingridient, price])
        time.sleep(1)
    except:
        continue

category = {}
for nutrtion_information in nutrtion_informations:
    for i in nutrtion_information[3]:
        category[i] = None

category = [i for i in category]

data_nutrtion_informations = {}
for i in category:
    data_nutrtion_informations[i] = []
data_nutrtion_informations['date'] = []
data_nutrtion_informations['names'] = []
data_nutrtion_informations['img_src'] = []
data_nutrtion_informations['img_directory_file'] = []
data_nutrtion_informations['category_food'] = []
data_nutrtion_informations['size'] = []
data_nutrtion_informations['ingridient'] = []
data_nutrtion_informations['price_food'] = []
for nutrtion_information in nutrtion_informations:
    data_nutrtion_informations['date'].append(date)
    data_nutrtion_informations['names'].append(nutrtion_information[0])
    data_nutrtion_informations['img_src'].append(nutrtion_information[1])
    data_nutrtion_informations['img_directory_file'].append(nutrtion_information[2])
    data_nutrtion_informations['category_food'].append(nutrtion_information[5])
    data_nutrtion_informations['size'].append(nutrtion_information[6])
    data_nutrtion_informations['ingridient'].append(nutrtion_information[7])
    data_nutrtion_informations['price_food'].append(nutrtion_information[8])
    for cat, val in zip(nutrtion_information[3],nutrtion_information[4]):
        data_nutrtion_informations[cat].append(val)
    for i in category:
        if not(i in nutrtion_information[3]):
            data_nutrtion_informations[i].append('Empty')

driver.close()
driver.quit()


for i in data_nutrtion_informations:
    print(data_nutrtion_informations[i])


pd.DataFrame(data_nutrtion_informations).to_excel(f'mcdonalds_nutrition_information_{str(date)}.xlsx')
