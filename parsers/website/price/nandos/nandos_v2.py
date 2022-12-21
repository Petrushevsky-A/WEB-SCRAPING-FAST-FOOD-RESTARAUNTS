from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

from database.database import DataBase

def get_item(driver):
    try:
        item = driver.find_element(By.XPATH, '//div[@class="inner"]//h3').get_attribute('innerHTML')
        return item
    except:
        return 'Not found'


def get_picture(driver):
    try:
        picture = driver.find_element(By.XPATH, '//div[@class="inner"]//img').get_attribute('src')
        return picture
    except:
        return 'Not found'


def get_product(driver, category_1, item, price):
    product = {
        'Start date': [datetime.now().strftime("%d.%m.%Y")],
        'End date': [datetime.now().strftime("%d.%m.%Y")],
        'Brand': ["Nando's"],
        'Address': [''],
        'City': [''],
        'Post_code': [''],
        'Segment': [''],
        'Category': [category_1[4:-5]],
        'Category 2': [''],
        'Category 3': [''],
        'Category 4': [''],
        'Item': [item],
        'Source': ['https://www.nandos.co.uk/'],
        'Region': ['UK'],
        'Price(£)': [price],
        'Status': ['on'],
        'Picture': [get_picture(driver)],
    }
    print(product)
    return product


def get_size(driver, category_1):
    data_dop = {}
    try:
        size = {
            'name': [f'{get_item(driver)} {i.get_attribute("innerHTML")}' for i in driver.find_elements(By.XPATH, '//table//tr/th')],
            'price': [i.get_attribute('innerHTML')[1:] for i in driver.find_elements(By.XPATH, '//table//tr/td')]
        }

        if len(size['name']):
            for i in range(len(size['name'])):
                data_size = get_product(driver, category_1, size['name'][i], size['price'][i])
                for key in data_size:
                    if key in data_dop:
                        data_dop[key] += data_size[key]
                    else:
                        data_dop[key] = data_size[key]

        else:
            price = driver.find_element(By.XPATH, '//div[@class="inner"]//div[@class="price"]').get_attribute('innerHTML')[1:]
            name = get_item(driver)
            data_dop = get_product(driver, category_1, name, price)

    except:
        print(f'ERROR: {category_1}')

    return data_dop


def get_category(driver, buttons, category_1):
    data = {}

    for button in buttons:
        try:
            data_dop = {}
            while 'Brand' not in data_dop:
                try:

                    button.click()
                    sleep(1)
                    data_dop = get_size(driver, category_1)
                    driver.find_element(By.XPATH, '//a[@class="close"]').click()

                    for key in data_dop:
                        if key in data:
                            data[key] += data_dop[key]
                        else:
                            data[key] = data_dop[key]
                except:
                    scroll_value = 100
                    scroll_by = f'window.scrollBy(0, {scroll_value});'
                    driver.execute_script(scroll_by)
                    sleep(0.2)

        except:
            print(button)
    return data


def configuring_driver():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    return driver


def get_nandinos_kids(driver, divs, category_1):
    subSection = ''
    sets = {}
    for div in divs:
        name = ''
        while name == '':
            if div.get_attribute('class') == 'subSection':
                subSection = div.get_attribute('innerHTML')
                name = subSection
                sets[subSection] = list()

            else:
                try:
                    div.click()
                    sleep(1)
                    name = driver.find_element(By.XPATH, '//div[@class="inner"]//h3').get_attribute('innerHTML')
                    sets[subSection].append(name)
                    driver.find_element(By.XPATH, '//a[@class="close"]').click()
                except:
                    scroll_value = 100
                    scroll_by = f'window.scrollBy(0, {scroll_value});'
                    driver.execute_script(scroll_by)
                    sleep(0.2)
    data = {}
    for mains in sets['Mains']:
        for sides in sets['Nandino sides']:
            for ireland in sets['Available in Northern Ireland']:
                for drink in sets['Dessert OR Drink']:
                    data_dop = get_product(driver, category_1, f'{mains}, {sides}, {ireland}, {drink}', '5.95')
                    for key in data_dop:
                        if key in data:
                            data[key] += data_dop[key]
                        else:
                            data[key] = data_dop[key]

    return data


def start():
    driver = configuring_driver()

    driver.get(url='https://www.nandos.co.uk/food/menu/')
    sleep(3)
    driver.find_element(By.XPATH, '//button[@id="truste-consent-required"]').click()
    sleep(1)

    id_sections = [i.get_attribute('id') for i in driver.find_elements(By.XPATH, '//section')]
    data_final = {}
    for id in id_sections:
        if id == 'section_nandinos-kids':
            divs = driver.find_elements(By.XPATH, f'//section[@id="section_nandinos-kids"]/div[2]/*')
            data = get_nandinos_kids(driver, divs, driver.find_element(By.XPATH, f'//section[@id="{id}"]/h2').get_attribute('innerHTML'))
        else:
            buttons = driver.find_elements(By.XPATH, f'//section[@id="{id}"]//button')
            data = get_category(driver, buttons, driver.find_element(By.XPATH, f'//section[@id="{id}"]/h2').get_attribute('innerHTML'))

        for key in data:
            if key in data_final:
                data_final[key] += data[key]
            else:
                data_final[key] = data[key]

    driver.close()
    driver.quit()
    data_frame = pd.DataFrame(data_final)
    # pd_data.to_excel(f'tables/Nandos_Price_{datetime.now().strftime("%d.%m.%Y")}.xlsx')
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_nandos_price')

def start_nandos_price_v2():
    start()
