import time
from datetime import datetime
import sqlite3
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
        try:
            driver.find_element(By.XPATH, '//div[@role="dialog"]//button[@type="button"]').click()
            time.sleep(2)
        except:
            print("Not found accept")
        pass


# Получение адреса ресторана
def get_address(driver, city):

    try:
        driver.find_element(By.XPATH,
                            '//*[contains(@class,"Menu")]//*[contains(@class,"Header")]//*[contains(text(),"Info")]').click()
        time.sleep(2)
        address = driver.find_element(By.XPATH, '(//div[contains(@id, "layout-list-map")]//div[contains(@class, "UIContentCard")]//div[contains(@class, "UILines")])[1]').text
    except:
        try:
            address = driver.find_element(By.XPATH, f'//*[contains(@id, "map")]//*[contains(text(), "{city}")]').text
        except:
            address = ''
    return address


# Получение названия бренда
def get_brand(driver):
    try:
        brand = driver.find_element(By.XPATH, '//h1').text.split(' - ')
        return brand[0]
    except:
        return "Npt found"


# олучение html-кодов по категориям
def get_html_category_list_foods(driver):
    return [i.get_attribute('innerHTML') for i in
            driver.find_elements(By.XPATH, '//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")]')]


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
                '//h3')]
            return "".join(text)
        except:
            return 'Not found'

    # Получение ссылки на картинку товара
    def get_image_food(self, html):
        try:
            html = etree.HTML(html)
            url_image = [i.get('style') for i in html.xpath('//div[contains(@style, "background-image")]')]
            return url_image[0][23:-3]
        except:
            return 'Not found'

    # Получение название товара
    def get_name_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath(
                '(//p)[1]')]
            return "".join(text)
        except:
            return 'Not found'

    # Получение цены товара
    def get_cost_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath('//span[contains(text(), "£")]')]
            text = "".join(text).replace('£', '')
            text.replace(',', '.')
            if len(text) > 5:
                text = text[:len(text)//2]
            return text
        except:
            return 'Not found'

    # Поллучение html-кодов карточек товаров
    def get_html_card_food(self) -> list["html"]:
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
            data_frame = pd.DataFrame([{
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
                'Source': 'deliveroo.co.uk',
                'Region': 'UK',
                'Price': cost,
                'Status': "on",
                'Picture': image_url,
            }])
            DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_deliveroo_price')
        return data


# Пролистывание страницы до конца, для подгрузки всех товаров
def scrolling_page(driver):
    for to_scrolling_element in driver.find_elements(By.XPATH, '//ul/li'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)


def parse(arg):
    try:
        url, post_code, city = arg
        print(f"PARSED {url}")

        # Открытие страницы ресторана
        driver = configuring_driver()
        driver.get(url=url)
        time.sleep(3)

        # Закрытие всех всплывающих окон
        accept_click(driver)

        # Поиск названия бренда и адреса ресторана
        brand = get_brand(driver)
        address = get_address(driver, city)

        # Пролистывание страницы для прогрузки всех товаров
        scrolling_page(driver)

        # Поиск html-кода категорий
        html_list_category_foods = get_html_category_list_foods(driver)

        # Сбор данных по категориям в список
        data = []
        for html_category in html_list_category_foods:
            try:
                menu = Parse_menu(html_list_category_foods=html_category,
                                  url=url,
                                  post_code=post_code,
                                  city=city,
                                  brand=brand,
                                  address=address,
                                  )

                data.append(menu())
            except Exception as ex:
                print(ex)

        # Запись данных в Excel
        data = sum(data, [])
        date = datetime.now().strftime("%d.%m.%Y")
        # pd.DataFrame(data).to_excel(f'tables/deliveroo_{brand}_{city}_price_{str(date)}.xlsx')
        # data_frame = pd.DataFrame(data).to_excel(f'tables/deliveroo_{brand}_{city}_price_{str(date)}.xlsx')
        # DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_nandos_price')
    except:
        pass





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
    data = DataBase().get_table('deliveroo_list_urls')
    urls_brands = []
    next(next(data)).apply(lambda x: urls_brands.append(tuple(x)), axis=1)
    with Pool(processes=1) as p:
        p.map(parse, urls_brands)


def start_deliveroo_price_v2():
    start()
