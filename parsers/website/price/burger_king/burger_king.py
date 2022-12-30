from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from multiprocessing import Pool
from database.database import DataBase
import setting

def get_picture(driver):
    try:
        picture = driver.find_element(By.XPATH, '//source[@data-testid="picture-source"]').get_attribute('srcset')
        picture = picture.split(' ')[0]
        return picture
    except:
        return 'Not found'


def get_name(driver):
    try:
        name = driver.find_element(By.XPATH, '//h1').get_attribute('innerHTML')
        return name
    except:
        return 'Not found'


def get_price(driver):
    price = driver.find_element(By.XPATH, '//h2//span[@data-testid="product-total-price"]').get_attribute('innerHTML')
    return price[1:]


def get_product(driver, city, post_code, category):
    product = {
        'Start date': [datetime.now().strftime("%d.%m.%Y")],
        'End date': [datetime.now().strftime("%d.%m.%Y")],
        'Brand': ['Burger King'],
        'Address': [''],
        'City': [city],
        'Postcode': [post_code],
        'Segment': [''],
        'Category': [category],
        'Category 2': [''],
        'Category 3': [''],
        'Category 4': [''],
        'Item': [get_name(driver)],
        'Source': ['https://www.burgerking.co.uk/'],
        'Region': ['UK'],
        'Price(£)': [get_price(driver)],
        'Status': ['on'],
        'Picture': [get_picture(driver)],
    }
    return product


def get_sizes(driver, city, post_code, category):
    data_meals = dict()
    sizes = driver.find_elements(By.XPATH, '//div[@data-testid="pickers"]/div[1]//div[@role="button"]')
    if len(sizes):
        for size in sizes:
            size.click()
            time.sleep(1)
            meals = driver.find_elements(By.XPATH, '//div[@data-testid="pickers"]/div[2]//div[@role="button"]')
            if len(meals):
                for meal in meals:
                    meal.click()
                    time.sleep(1)
                    data_size = get_product(driver, city, post_code, category)
                    for key in data_size:
                        if key in data_meals:
                            data_meals[key] += data_size[key]
                        else:
                            data_meals[key] = data_size[key]
            else:
                data_size = get_product(driver, city, post_code, category)
                for key in data_size:
                    if key in data_meals:
                        data_meals[key] += data_size[key]
                    else:
                        data_meals[key] = data_size[key]
    else:
        data_meals = get_product(driver, city, post_code, category)
    return data_meals


def get_categories(driver, city, post_code):
    category = {
        'url': [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//a[@class="tile-linkbk__TileListLink-fepcm3-2 fGbzQA"]')],
        'name': [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//h2[@class="tilebk__TileListHeader-sc-11x1xm1-4 cFFcdJ"]')]
    }
    data = dict()
    for i in range(len(category['url'])):
        try:
            driver.get(url=category['url'][i])
            time.sleep(5)
            products = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//a[@class="tile-linkbk__TileListLink-fepcm3-2 dAxxU"]')]
            k = 1
            for url in products:
                try:
                    driver.get(url=url)
                    time.sleep(5)
                    data_dop = get_sizes(driver, city, post_code, category['name'][i])
                    for key in data_dop:
                        if key in data:
                            data[key] += data_dop[key]
                        else:
                            data[key] = data_dop[key]
                    k += 1
                except:
                    print(f'ERROR {url}, {category["name"][i]} {k} {post_code} {city}')
        except:
            print(f'ERROR {category["url"][i]} {post_code} {city}')
    pd_data = pd.DataFrame(data, index=[0])
    DataBase().to_stg_table(data_frame=pd_data, name_stg_table='stg_burger_king_price')


def parse(post_code, city):
    url = 'https://www.burgerking.co.uk/store-locator?navbar1'
    try:
        driver = configuring_driver()
        print(f"PARSED {url} {city}")
        print(f'post_code {post_code}')
        driver.get(url=url)
        time.sleep(10)
        driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(post_code)
        time.sleep(4)
        driver.find_element(By.XPATH, '//ul//button').click()
        time.sleep(5)


        buttons = driver.find_elements(By.XPATH,
                                       '//div[@class="store-card-liststyled__StoreCardListWrapper-mw4ua4-0 hitVxO"]//button[@class="unstyled-button__UnstyledButton-sc-15lagcm-0 store-cardstyled__CardButton-sc-1s810z7-1 kqyAAj jqQWFE"]')
        for button in buttons:
            button.click()
            time.sleep(1)
            try:
                but = driver.find_element(By.XPATH, '//div[@class="build__BaseBox-b7zorw-81 LzNDx"]/div[2]/button')
                if but.get_attribute('aria-disabled') == 'false':
                    but.click()
                    time.sleep(10)
                    get_categories(driver, city, post_code)
                    break
                else:
                    continue

            except:
                continue


    except ValueError as ex:
        print(ex)
        print(f"ERROR {url}")
    finally:
        driver.close()
        driver.quit()


def configuring_driver():
    options = Options()
    tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
    path = setting.SELENIUM['path']
    options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    return driver


def main():
    data = next(next(DataBase().get_table(name_table='burger_king_data')))
    data = data.itertuples(index=False, name=None)
    data = tuple(data)
    print(data)
    with Pool(processes=1) as p:
        p.starmap(parse, data)


def start_burger_king_price():
    main()

