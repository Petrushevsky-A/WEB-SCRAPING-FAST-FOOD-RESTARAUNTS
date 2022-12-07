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
urls = pd.read_excel(f"burger_king_url_foods_{str(date)}.xlsx")["links"]
category = pd.read_excel(f"burger_king_url_foods_{str(date)}.xlsx")["category"]



nutrtion_informations = []
try:
    for url, category_food in zip(urls, category):
        try:
            print(url)
            driver.get(url=url)
            time.sleep(5)


            # *[contains(@class, "guidebk")]
            ingridient = "Not found"
            try:
                # ingridient = driver.find_element(By.XPATH, '//div[contains(@class, "panel")]').get_attribute('innerHTML')
                ingridient = driver.find_element(By.XPATH,'//div[contains(@id, "accordion-content")]/div[1]/p[1]').get_attribute('innerHTML')
                print(ingridient)
            except:
                print(f"ERROR: {ingridient}")
            size = "empty"
            try:
                size = driver.find_element(By.XPATH,'//div[contains(@class, "dFEDhe")]/following::div/div/h3').get_attribute('innerHTML')
                print(size)
            except:
                print(f"ERROR: {size}")
            food_nutritional_information = driver.find_element(By.XPATH, '//button[contains(@class, "text-with-arrow")]')

            driver.execute_script("arguments[0].click();", food_nutritional_information)
            time.sleep(2)


            name = driver.find_element(By.XPATH, '//div[contains(@class, "content-wrapper")]/h3[contains(@class, "item-name")]').text
            print(name)


            category_nutrtion_information = []
            value_nutrtion_information = []

            try:
                category_nutrtion_information = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@class, "content-wrapper")]/div[contains(@class, "nutrient__Nutrient")]/span[1]')][:7]
                value_nutrtion_information = [i.text for i in driver.find_elements(By.XPATH, '//div[contains(@class, "content-wrapper")]/div[contains(@class, "nutrient__Nutrient")]/span[2]')][:7]
            except:
                print(f"ERROR {name}")




            print(category_nutrtion_information)
            print(value_nutrtion_information)


            time.sleep(2)


            # Забрать ценник
            price = "Not found"
            try:
                price = driver.find_element(By.XPATH, '//span[contains(@data-testid, "product-total-price")]').text
            except:
                print(f'ERROR PRICE')

            list_img_file = []
            list_img_src = []

            src_img = driver.find_element(By.XPATH, '//source[@data-testid="picture-source"]').get_attribute("srcset").split(',')[0][:-5]

            print(src_img)
            directory = "burger_king_img"
            name_img = name
            try:
                reponse_img = requests.get(src_img)
                if reponse_img.status_code == 200:
                    with open(f"./{directory}/{name_img}.png", "wb") as file:
                        file.write(reponse_img.content)
            except:
                print(f"ERROR {src_img}")


            print(f'ingridient: {ingridient}')


            nutrtion_informations.append([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, size, ingridient, price])
            print([name, src_img, f"./{directory}/{name_img}.jpg", category_nutrtion_information, value_nutrtion_information, category_food, size, ingridient, price])
            time.sleep(1)
        except:
            continue
except:
    pass
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





pd.DataFrame(data_nutrtion_informations).to_excel(f'burger_king_nutrition_information_{str(date)}.xlsx')
