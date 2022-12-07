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


url = 'https://www.costa.co.uk/menu'
# category = pd.read_excel("greggs_url_foods.xlsx")["category"]
driver.get(url = url)
time.sleep(5)
driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
time.sleep(1)
sidebar = driver.find_elements(By.XPATH, '//div[contains(@class, "pageSelect")]//button')

nutrtion_informations = []

for id_side, side in enumerate(sidebar, 1):
    side.click()
    time.sleep(1)
    for id_cat, val_cat in enumerate(driver.find_elements(By.XPATH, '//div[contains(@class, "categoryHeader")]'), 1):
        category = val_cat.get_attribute('innerHTML')
        elements = driver.find_elements(By.XPATH, f'//div/div[contains(@class, "productList")][{id_cat}]/div[@class="container"]/div[contains(@class, "productItem")]')
        for id_food, val_food in enumerate(elements, 1):
            val_food.click()
            time.sleep(3)
            try:
                name = driver.find_element(By.XPATH, '//div[@class="componentWrapperWhite"]/h1').get_attribute(
                    'innerHTML')
                print(name)
            except:
                name = driver.find_element(By.XPATH, '//h1').get_attribute('innerHTML')
                print(name)

            category_nutrtion_information = []
            value_nutrtion_information = []
            size_name = []
            try:
                try:
                    sizes = driver.find_elements(By.XPATH, '//div[@class="filterGroup size"]//button')
                    if len(sizes) ==0:
                        raise sizes
                    print(f'sizes: {[i.text for i in sizes]}')
                except:
                    sizes = ["empty"]
                    print(f'sizes : {sizes}')
                try:
                    for size in sizes:
                        size.click()
                        time.sleep(1)
                        try:

                            category_nutrtion_information.append([i.text for i in driver.find_elements(By.XPATH,
                                                                                                       '//div[@class="content"]/div[contains(@class, "nutritionTable")]/table/tbody/tr/td[1]')])
                            value_nutrtion_information.append([i.text for i in driver.find_elements(By.XPATH,
                                                                                                    '//div[@class="content"]/div[contains(@class, "nutritionTable")]/table/tbody/tr/td[3]')])
                            size_name.append(size.text)
                        except:
                            print(f"ERROR {name}")
                except:
                    try:

                        category_nutrtion_information.append([i.text for i in driver.find_elements(By.XPATH,
                                                                                                   '//div[@class="content"]/div[contains(@class, "nutritionTable")]/table/tbody/tr/td[1]')])
                        value_nutrtion_information.append([i.text for i in driver.find_elements(By.XPATH,
                                                                                                '//div[@class="content"]/div[contains(@class, "nutritionTable")]/table/tbody/tr/td[3]')])
                        size_name.append(size)
                    except:
                        print(f"ERROR {name}")
                print(name)
            except:
                pass

            print(category_nutrtion_information)
            print(value_nutrtion_information)
            print(size_name)

            time.sleep(2)


            list_img_file = []
            list_img_src = []

            src_img = driver.find_element(By.XPATH, '//div[@class="fixedImage"]/img').get_attribute("src")

            print(src_img)
            directory = "costa_img"
            name_img = name.strip()
            try:
                reponse_img = requests.get(f"https://www.costa.co.uk{src_img}")
                if reponse_img.status_code == 200:
                    with open(f"{directory}/{name_img}.png", "wb") as file:
                        file.write(reponse_img.content)
            except:
                print(f"ERROR {src_img}")
            ingridient = "empty"
            try:
                ingridient = driver.find_element(By.XPATH, '//div[@class="ingredients"]').text
            except:
                print(f"ERROR: {ingridient}")
            print(f'ingridient: {ingridient}')
            try:
                description = driver.find_element(By.XPATH, '//div[@class="description"]/p[1]').text
            except:
                description = 'Not found'

            print(description)

            driver.find_element(By.XPATH, '//button[@class="closeButton"]').click()

            for id, val in enumerate(size_name):
                nutrtion_informations.append([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information[id], value_nutrtion_information[id], category, val, ingridient, description])
                print([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information[id], value_nutrtion_information[id], category, val, ingridient, description])
            time.sleep(1)


category = {}
for nutrtion_information in nutrtion_informations:
    for i in nutrtion_information[3]:
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
data_nutrtion_informations['description'] = []
for nutrtion_information in nutrtion_informations:
    data_nutrtion_informations['date'].append(date)
    data_nutrtion_informations['names'].append(nutrtion_information[0])
    data_nutrtion_informations['img_src'].append(nutrtion_information[1])
    data_nutrtion_informations['img_directory_file'].append(nutrtion_information[2])
    data_nutrtion_informations['category_food'].append(nutrtion_information[5])
    data_nutrtion_informations['size'].append(nutrtion_information[6])
    data_nutrtion_informations['ingridient'].append(nutrtion_information[7])
    data_nutrtion_informations['description'].append(nutrtion_information[8])
    for cat, val in zip(nutrtion_information[3],nutrtion_information[4]):
        data_nutrtion_informations[cat].append(val)
    for i in category:
        if not(i in nutrtion_information[3]):
            data_nutrtion_informations[i].append('Empty')

driver.close()
driver.quit()





pd.DataFrame(data_nutrtion_informations).to_excel(f'costa_nutrition_information_{str(date)}.xlsx')
