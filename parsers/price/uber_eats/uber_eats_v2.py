import sqlite3
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from multiprocessing import Pool
from lxml import etree

from database.database import DataBase


# Закрытие всех всплывающих окон
def accept_click(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(2)
    except:
        print("Not found accept")
        pass


# Закрытие всех всплывающих окон
def close_popup(driver):
    try:
        driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        time.sleep(2)
    except:
        pass


# Получение адреса ресторана
def get_address(driver, city):
    try:
        address = driver.find_element(By.XPATH,
                                      f'//span[contains(text(),"{city}")]').text
    except:
        try:
            address = driver.find_element(By.XPATH,
                                          '(//h1/parent::div//span[contains(text(), ",")])[1]').text
        except:
            address = ''
    return address


# Получение названия бренда
def get_brand(driver):
    try:
        brand = driver.find_element(By.XPATH, '//h1').get_attribute('innerHTML')
        return brand
    except Exception as ex:
        print(ex)
        return 'Not found'


# олучение html-кодов по категориям
def get_html_category_list_foods(driver):
    return [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '(//main//ul)[1]/li')]


class Parse_menu():

    def __init__(self, html_list_category_foods, post_code, url, city, brand, address):
        self.html = etree.HTML(html_list_category_foods)
        self.url = url
        self.post_code = post_code
        self.city = city
        self.brand = brand
        self.address = address

    # Получение название категории
    def get_name_category(self):
        try:
            text = [i.text for i in self.html.xpath(
                '(//div)[1]')]
            return "".join(text)
        except:
            return 'Not found'

    # Получение ссылки на картинку товара
    def get_image_food(self, html):
        try:
            html = etree.HTML(html)
            url_image = [i.get('src') for i in html.xpath('//img')]
            return url_image[0]
        except:
            return 'Not found'

    # Получение названия товара
    def get_name_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath(
                '(//span)[1]')]
            return "".join(text)
        except:
            return 'Not found'

    # Получение цены товара
    def get_cost_food(self, html):
        try:
            html = etree.HTML(html)

            text = [i.text[2:] for i in html.xpath('(//span)[2]')]
            return "".join(text)
        except:
            try:
                text = [i.text[2:] for i in html.xpath('(//span)[3]')]
                return "".join(text)
            except:
                try:
                    text = [i.text[2:] for i in html.xpath('(//span)[4]')]
                    return "".join(text)
                except:
                    try:
                        text = [i.text[2:] for i in html.xpath('(//span)[5]')]
                        return "".join(text)
                    except Exception as ex:
                        print(ex)
                        return 'Not found'

    # Поллучение html-кодов карточек товаров
    def get_html_card_food(self) -> list['html']:
        try:
            text = [etree.tostring(i) for i in self.html.xpath(
                '//li')]
            return text
        except:
            return ['Not found']

    def __call__(self, *args, **kwargs):

        # Получение даты, пост-кода, города, бренда, адреса и названия категории
        date = datetime.now().strftime("%d.%m.%Y")
        post_code = self.post_code
        city = self.city
        brand = self.brand
        address = self.address
        name_category = self.get_name_category()

        # Получение html-кодов карточек товаров
        html_card_food = self.get_html_card_food()
        data = []

        # Разбор каждой карточки товара
        for val in html_card_food:

            # Получение наименование позиции, ссылки на картинку и цены
            name = self.get_name_food(val)
            image_url = self.get_image_food(val)
            cost = self.get_cost_food(val)



            # Запись одной пазиции в словарь, для добавления в Excel
            data.append({
                'Start date': date,
                'End date': date,
                'Brand': brand,
                'Address': address,
                'City': city,
                'Post_code': post_code,
                'Segment': '',
                'Category': name_category,
                'Category 2': '',
                'Category 3': '',
                'Category 4': '',
                'Item': name,
                'Source': 'ubereats.com',
                'Region': 'UK',
                'Price(£)': cost,
                'Status': "on",
                'Picture': image_url,

            })
        return data


# Пролистывание страницы до конца, для подгрузки всех товаров
def scrolling_page(driver):
    for to_scrolling_element in driver.find_elements(By.XPATH, '(//main//ul)[1]/li'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)


# Получение элементов кнопок
def next_page(driver) -> list["Selenium element"]:
    try:
        return driver.find_elements(By.XPATH, '//main/div/div/a/')
    except:
        return ["123"]


def parse(arg):
    url, post_code, city = arg
    print(f"PARSED {url}")
    driver = configuring_driver()

    # Открытие страницы ресторана
    driver.get(url=url)
    time.sleep(3)

    # Закрытие всех всплывающих окон
    accept_click(driver)
    close_popup(driver)

    # Получение названия бренда и адреса
    brand = get_brand(driver)
    address = get_address(driver, city)

    # Получение всех кнопок
    pages = next_page(driver)

    html_list_category_foods = []

    # Пролистывание всех страниц и сбор html-кодов страниц
    for page in pages:
        try:
            page.click()
            time.sleep(2)
        except:
            pass
        scrolling_page(driver)
        html_list_category_foods.append(get_html_category_list_foods(driver))
    html_list_category_foods = sum(html_list_category_foods, [])

    # Перебор html-кодрв по категориям
    data = []
    for html_category in html_list_category_foods:
        menu = Parse_menu(html_list_category_foods=html_category,
                          url=url,
                          post_code=post_code,
                          city=city,
                          brand=brand,
                          address=address,
                          )
        data.append(menu())

    # Запись данных с ресторана в Excel
    data = sum(data, [])
    date = datetime.now().strftime("%d.%m.%Y")
    # pd.DataFrame(data).to_excel(f'tables/uber_eats_{brand}_{post_code}_result_menu_price_{str(date)}.xlsx')
    data_frame = pd.DataFrame(data)
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_uber_eats_price')




# Настройка хромдрайвера
def configuring_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    return driver


# Начало парсинга по ссылкам из таблицы и создание таблицы в базе данных
def start():
    data = DataBase().get_table('uber_eats_list_url')
    urls_brands = []
    next(next(data)).apply(lambda x: urls_brands.append(tuple(x)), axis=1)
    with Pool(processes=3) as p:
        p.map(parse, urls_brands)


def start_uber_eats_price_v2():
    start()
