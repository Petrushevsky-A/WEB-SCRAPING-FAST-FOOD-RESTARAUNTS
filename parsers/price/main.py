import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
import requests
import numpy as np
from multiprocessing import Pool


options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

path = r'chromedriver.exe'


urls = pd.read_excel('list_urls.xlsx')['links']
brands = pd.read_excel('list_urls.xlsx')['brands']

def parse(url, brand):
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url=url)
    time.sleep(3)
    print(f"PARSED {url}")
    try:
        driver.find_element(By.XPATH, '//button[@data-test-id="accept-all-cookies-button"]').click()
        time.sleep(8)
    except:
        pass





    name_place = driver.find_element(By.XPATH, '//h1[@data-js-test="restaurant-heading"]').text
    address = driver.find_element(By.XPATH, '//span[@data-js-test="header-restaurantAddress"]').text
    post_code = address.split(',')[-1].strip()
    city = address.split(',')[-2].strip()

    print(url)
    print(brand)
    print(name_place)
    print(address)
    print(post_code)
    print(city)
    menu_list = []


    categorys = driver.find_elements(By.XPATH,  '//h2[@data-test-id="menu-category-heading"]')
    if len(categorys) == 0:
        driver.close()
        driver.quit()

        pd.DataFrame({
            'brand': [brand],
            'post_code': [post_code],
            'url': [url],
        }).to_excel(f'ERROR_{brand}_{post_code}_result_menu_price.xlsx')
        return None

    for id_cat, category in enumerate(categorys, 1):
        text_category = category.get_attribute('innerHTML').strip()
        print(text_category)
        if 'Allergen' in text_category or 'Limited' in text_category:
            continue


        for id_food, food in enumerate(driver.find_elements(By.XPATH, f'//section[@data-test-id="menu-category-item"][{id_cat}]//div[@data-js-test="menu-item"]'), 1):



            try:
                name = driver.find_element(By.XPATH, f'//section[@data-test-id="menu-category-item"][{id_cat}]//div[@data-js-test="menu-item"][{id_food}]//h3[@data-js-test="menu-item-name"]').get_attribute('innerHTML').replace("<!---->", "").strip()
            except:
                name = 'Not found'
            print(name)
            try:
                price = driver.find_element(By.XPATH, f'//section[@data-test-id="menu-category-item"][{id_cat}]//div[@data-js-test="menu-item"][{id_food}]//p[@data-js-test="menu-item-price"]').get_attribute('innerHTML').strip()
            except:
                price = 'Not found'
            print(price)
            try:

                image = driver.find_element(By.XPATH, f'//section[@data-test-id="menu-category-item"][{id_cat}]//div[@data-js-test="menu-item"][{id_food}]//div[contains(@class, "c-menuItems-imageContainer")]/img')
                driver.execute_script("arguments[0].scrollIntoView();", image)
                time.sleep(1)
                image_source = image.get_attribute('src')
                directory = f"./{brand}/{name}.png"
                try:
                    reponse_img = requests.get(image_source)
                    if reponse_img.status_code == 200:
                        with open(directory, "wb") as file:
                            file.write(reponse_img.content)
                except:
                    print(f"ERROR {image_source}")
            except:
                image_source = 'Not found'
                directory = 'Not found'
            print(image_source)
            print(directory)
            try:
                description = driver.find_element(By.XPATH,f'//section[@data-test-id="menu-category-item"][{id_cat}]//div[@data-js-test="menu-item"][{id_food}]//p[@data-js-test="menu-item-description"]').get_attribute('innerHTML').replace("<!---->", "").strip()
            except:
                description = 'Not found'
            print(description)
            menu_list.append([brand,name_place,address,city,post_code,text_category, name, price, image_source, directory, description, url])

        print(len(menu_list))

        driver.close()
        driver.quit()

        menu_list = np.array(menu_list).T.tolist()


        data = {
            'brand':menu_list[0],
            'name_place':menu_list[1],
            'address':menu_list[2],
            'city':menu_list[3],
            'post_code':menu_list[4],
            'text_category':menu_list[5],
            'name':menu_list[6],
            'price':menu_list[7],
            'image_source':menu_list[8],
            'directory':menu_list[9],
            'description':menu_list[10],
            'url':menu_list[11],
        }

        pd.DataFrame(data).to_excel(f'{brand}_{post_code}_result_menu_price.xlsx')



if __name__ == '__main__':

    with Pool(processes=1) as p:
        p.map(parse, urls)