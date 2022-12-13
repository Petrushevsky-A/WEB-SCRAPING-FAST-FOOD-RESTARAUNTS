import time
from datetime import datetime
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from multiprocessing import Pool

from database.database import DataBase

# Закрытие всех всплывающих окон
def accept_click(driver):
    try:
        driver.find_element(By.XPATH, '//button[@data-test-id="accept-all-cookies-button"]').click()
        time.sleep(1)
    except:
        pass


# Получение адреса ресторана
def get_address(driver):

    try:
        address = driver.find_element(By.XPATH, '//span[@data-js-test="header-restaurantAddress"]').get_attribute('innerHTML')
        return address
    except:
        return 'Not found'


def get_post_code(address):
    if address != 'Not found':
        post_code = address.split(',')[-1].strip()
    else:
        post_code = 'Not found'
    return post_code


def get_city(address):
    if address != 'Not found':
        city = address.split(',')[-1].strip()
    else:
        city = 'Not found'
    return city


def if_close_brand(driver):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Order for later")]').click()
        time.sleep(2)
    except:
        pass


def add_to_table(date, brand, address, city, post_code, category, name, price, status, image_url):
    product = {
        'Start date': date,
        'End date': date,
        'Brand': brand,
        'Address': address,
        'City': city,
        'Post_code': post_code,
        'Segment': '',
        'Category': category,
        'Category 2': '',
        'Category 3': '',
        'Category 4': '',
        'Item': name,
        'Source': 'deliveroo.co.uk',
        'Region': 'UK',
        'Price': price,
        'Status': status,
        'Picture': image_url,
    }
    return product


class Parse_menu():

    def __init__(self, driver, id_category, category, post_code, url, city, brand, address):
        self.driver = driver
        self.id_category = id_category
        self.category = category
        self.url = url
        self.post_code = post_code
        self.city = city
        self.brand = brand
        self.address = address

    def get_id_foods(self):
        return [i.get_attribute('data-product-id') for i in self.driver.find_elements(By.XPATH, f'//section[@data-test-id="menu-category-item"][{self.id_category}]/div')]

    # Получение ссылки на картинку товара
    def get_image(self, id_food):
        try:
            image = self.driver.find_element(By.XPATH, f'//div[@data-product-id="{id_food}"]//div[@class="c-menuItems-imageContainer"]//img').get_attribute('src')
            if image == '':
                image = 'Not found'
        except:
            image = 'Not found'
        return image

    def get_image_subway(self):
        try:
            image = self.driver.find_element(By.XPATH, '//div[@role="document"]//img').get_attribute('src')
        except:
            image = 'Not found'
        return image

    # Получение название товара
    def get_name(self, id_food):
        try:
            name = self.driver.find_element(By.XPATH, f'//div[@data-product-id="{id_food}"]//h3').get_attribute('innerHTML').replace('<!---->', '').strip()
        except:
            name = 'Not found'
        return name

    def get_name_subway(self):
        try:
            name = self.driver.find_element(By.XPATH, '//span[@class="c-stickyHeader-title u-text-truncate"]').get_attribute('innerHTML').strip()
        except:
            name = self.driver.find_element(By.XPATH, '//h1[@data-test-id="modal-title"]/span/span').get_attribute('innerHTML').strip()
        return name

    # Получение цены товара
    def get_price(self, id_food):
        try:
            price = self.driver.find_element(By.XPATH, f'//div[@data-product-id="{id_food}"]//p[@data-js-test="menu-item-price"]').get_attribute(
                'innerHTML').strip()
            if price[0] == 'f':
                pass
            elif price == 'Unavailable':
                price = 'Not found'
            else:
                price = price[1:]
            price.replace(',', '.')
        except Exception as ex:
            print(ex)
            price = 'Not found'
        return price

    def __call__(self, *args, **kwargs):

        # Получение даты, пост-кода, города, бренда, адреса и названия категории
        date = datetime.now().strftime("%d.%m.%Y")
        post_code = self.post_code
        city = self.city
        brand = self.brand
        address = self.address
        category = self.category

        # Получение html-кодов карточек товаров
        id_foods = self.get_id_foods()
        data = []

        # Разбор каждой карточки товара
        for id_food in id_foods:

            # Получение наименование позиции, ссылки на картинку и цены
            price = self.get_price(id_food)

            if price[0] == 'f' and brand == 'Subway':
                k = 1
                while k:
                    try:
                        self.driver.find_element(By.XPATH, f'//div[@data-product-id="{id_food}"]/button').click()
                        time.sleep(2)
                        if_close_brand(self.driver)

                        image_url = self.get_image_subway()
                        status = 'on'
                        name = self.get_name_subway()

                        try:
                            if self.driver.find_element(By.XPATH, '//span[@class="c-itemSelector-section-heading-title"]').get_attribute('innerHTML').strip() == 'Choose one':
                                sizes = [i.get_attribute('innerHTML').strip() for i in self.driver.find_elements(By.XPATH, '//div[@data-js="itemSelector-section-row"]//label//span[@class="c-itemSelector-section-name"]/span')]
                                for i in range(0, len(sizes), 2):
                                    name_size = f'{name} {sizes[i]}'
                                    price = sizes[i + 1][1:]
                                    data.append(add_to_table(date, brand, address, city, post_code, category, name_size, price, status, image_url))
                            else:
                                price = self.driver.find_element(By.XPATH, '//p[@class="c-itemSelector-price"]').get_attribute('innerHTML').replace('<!---->', '').strip()[1:]
                                data.append(add_to_table(date, brand, address, city, post_code, category, name, price, status, image_url))
                        except:
                            price = self.driver.find_element(By.XPATH, '//p[@class="c-itemSelector-price"]').get_attribute('innerHTML').replace('<!---->', '').strip()[1:]
                            data.append(add_to_table(date, brand, address, city, post_code, category, name, price, status, image_url))

                        self.driver.find_element(By.XPATH, '//button[@data-test-id="close-modal"]').click()
                        time.sleep(0.8)
                        k = 0
                    except:
                        pass

            else:
                status = 'on'
                name = self.get_name(id_food)
                image_url = self.get_image(id_food)
                if price[0] == 'f':
                    price = price[6:]
                elif price == 'Not found':
                    status = 'off'

                # Добавление одной позиции в базу данных

                # data_frame = pd.DataFrame({
                #     'start_date': date,
                #     'end_date': date,
                #     'brand': brand,
                #     'address': address,
                #     'city': city,
                #     'post_code': post_code,
                #     'segment': '',
                #     'category': category,
                #     'category_2': '',
                #     'category_3': '',
                #     'category_4': '',
                #     'item': name,
                #     'source': 'deliveroo.co.uk',
                #     'region': 'UK',
                #     'price': price,
                #     'status': 'on',
                #     'picture': image_url,
                # })
                #
                # DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_just_eats_price')
                # Запись одной пазиции в словарь, для добавления в Excel
                data.append(add_to_table(date, brand, address, city, post_code, category, name, price, status, image_url))
        return data


# Пролистывание страницы до конца, для подгрузки всех товаров
def scrolling_page(driver):
    for to_scrolling_element in driver.find_elements(By.XPATH, '//ul/li'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)


def parse(arg):
    try:
        url, brand = arg
        print(f"PARSED {url}")

        # Открытие страницы ресторана
        driver = configuring_driver()
        driver.get(url=url)
        time.sleep(3)

        # Закрытие всех всплывающих окон
        accept_click(driver)

        # Поиск названия бренда и адреса ресторана
        address = get_address(driver)
        city = get_city(address)
        post_code = get_post_code(address)

        # Пролистывание страницы для прогрузки всех товаров
        scrolling_page(driver)

        # Сбор данных по категориям в список
        data = []
        for id_category, category_html in enumerate(driver.find_elements(By.XPATH, '//section[@data-test-id="menu-category-item"]/header/button/h2'), 1):
            try:
                category = category_html.get_attribute('innerHTML').strip()
                if 'Allergen' in category or 'Limited' in category:
                    continue
                menu = Parse_menu(driver=driver,
                                  id_category=id_category,
                                  category=category,
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
        # pd.DataFrame(data).to_excel(f'tables/just_eats_{brand}_{city}_price_{str(date)}.xlsx')
        data_frame = pd.DataFrame(data)
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_just_eats_price')
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
    data = DataBase().get_table('just_eats_list')
    urls_brands = []
    next(next(data)).apply(lambda x: urls_brands.append(tuple(x)), axis=1)
    with Pool(processes=1) as p:
        p.map(parse, urls_brands[35:])


def start_just_eats_price_v2():
    start()
