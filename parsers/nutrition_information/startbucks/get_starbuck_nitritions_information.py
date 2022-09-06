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
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)

date = datetime.now().strftime("%d.%m.%Y")
urls = pd.read_excel(f"starbucks_url_foods_{str(date)}.xlsx")["links"]

nutrtion_informations = []

list_img_file = []
list_img_src = []
for url in urls:
    try:

        driver.get(url = url)

        time.sleep(10)
        name = driver.find_element(By.XPATH, '//div[@class="wrapper"]//h2[contains(@class, "product-title")]').get_attribute("innerHTML")
        print(name)

        # добавить трай
        category_nutrtion_information = [i.get_attribute("innerHTML").strip() for i in driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-information")]//span[contains(@class, "copy-02")]')]
        value_nutrtion_information = [i.get_attribute("innerHTML").strip() for i in driver.find_elements(By.XPATH, '//div[contains(@class, "nutrition-information")]//span[@class = "nutritional-value"]')]
        print(category_nutrtion_information)
        print(value_nutrtion_information)

        category_food = " ".join([i.text for i in driver.find_elements(By.XPATH, '//div[@data-component="breadcrumbs"]//span')])
        ingridient = "empty"
        try:
            ingridient = driver.find_element(By.XPATH,
                                             '//p[contains(@class, "product-description")]').text
        except:
            print(f"ERROR: {ingridient}")

        # добавить трай
        src_img = driver.find_element(By.XPATH, '//picture[@class="image"]/img').get_attribute("data-src")

        print(src_img)
        reponse_img = requests.get(src_img)
        name_img = name
        directory = "starbucks_img"
        if reponse_img.status_code == 200:
            with open(f"./{directory}/{name_img}.jpg", "wb") as file:
                file.write(reponse_img.content)

        nutrtion_informations.append([name,src_img,f"./{directory}/{name_img}.jpg",category_nutrtion_information, value_nutrtion_information, category_food, ingridient])
    except:
        print(f"ERROR: {url}")
        continue

category = {}
for nutrtion_information in nutrtion_informations:
    for i in nutrtion_information[3]:
        print(i)
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
data_nutrtion_informations['ingridient'] = []
for nutrtion_information in nutrtion_informations:
    data_nutrtion_informations['date'].append(date)
    data_nutrtion_informations['names'].append(nutrtion_information[0])
    data_nutrtion_informations['img_src'].append(nutrtion_information[1])
    data_nutrtion_informations['img_directory_file'].append(nutrtion_information[2])
    data_nutrtion_informations['category_food'].append(nutrtion_information[5])
    data_nutrtion_informations['ingridient'].append(nutrtion_information[6])
    for cat, val in zip(nutrtion_information[3],nutrtion_information[4]):
        data_nutrtion_informations[cat].append(val)
    for i in category:
        if not(i in nutrtion_information[3]):
            data_nutrtion_informations[i].append('Empty')

driver.close()
driver.quit()





pd.DataFrame(data_nutrtion_informations).to_excel(f'starbucks_nutrition_information_{str(date)}.xlsx')