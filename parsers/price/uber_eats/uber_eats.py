import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
import requests
import numpy as np
from multiprocessing import Pool
from lxml import etree
import re

from database.database import DataBase

def accept_click(driver):
    # $x('//button[contains(text(), "Accept")]')
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(2)
    except:
        print("Not found accept")
        pass

def get_address(driver, city):

    try:
        address = driver.find_element(By.XPATH,
                            f'//span[contains(text(),"{city}")]').text
    except:
        try:
            # $x('(//h1/parent::div//span[contains(text(), ",")])[1]')
            address = driver.find_element(By.XPATH,
                                          '(//h1/parent::div//span[contains(text(), ",")])[1]').text
        except:
            address = ''
    return address

def get_brand(driver):
    # brand = name place
    brand = driver.find_element(By.XPATH, '//h1').text
    return brand

def get_html_category_list_foods(driver):
    # $x('//main//ul')[1:]
    # '(//main//ul)[1]/li'
    return [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '(//main//ul)[1]/li')]


def close_popup(driver):
    # $x('//button[@aria-label="Close"]')
    try:
        driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        time.sleep(2)
    except:
        pass
class Parse_menu():

    # $x('(//main//ul)[2]/li[1]//span')
    # $x('(//main//ul)[2]/li[1]//img')
    # $x('//span[contains(text(), "£")]').map(i= > i.textContent) split('•')

    def __init__(self, html_list_category_foods, post_code , url, city, brand, address):
        self.html = etree.HTML(html_list_category_foods)
        self.url = url
        self.post_code = post_code
        self.city = city
        self.brand = brand
        self.address = address

    def get_name_category(self):
        try:
            text = [i.text for i in self.html.xpath(
                '(//div)[1]')]
            return "".join(text)
        except:
            return 'Not found'

    def get_image_food(self, html):
        try:
            html = etree.HTML(html)
            url_image = [i.get('src') for i in html.xpath('//img')]
            return url_image[0]
        except:
            return 'Not found'

    def get_name_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath(
                '(//span)[1]')]
            return "".join(text)
        except:
            return 'Not found'


    # def get_description_food(self, html):
    #     try:
    #         html = etree.HTML(html)
    #         text = [i.text for i in html.xpath(
    #             '(//p)[2]')]
    #         return "".join(text)
    #     except:
    #         return 'Not found'

    def get_cost_food(self, html):
        try:
            # '//span[contains(text(), "£")]'
            html = etree.HTML(html)
            # html = html.fromstring(html)
            # text = [i.text for i in html.xpath("//span[contains(text(), '£')]")]
            # text = [i.text for i in html.xpath("//span[class = 'i8 ek i9 ba bx dk c5 ax']")]
            # text = [etree.tostring(i) for i in html.xpath('//*[contains(text(), "£")]')]
            # text = [etree.tostring(i) for i in html.xpath('//*[contains(text(), "&#8364;")]')]
            text = etree.tostring(html)
            # result = re.search(r'>&#8364\;(\d*.\d*)<', str(text)).group(1)
            try:
                result = re.findall(r'>&#8364\;(.{0,8})<\/span', str(text))[0]
            except:
                try:
                    result = re.findall(r'>£(.{0,6})<\/span', str(text))[0]
                except:
                    result = re.findall(r'>&#163\;(.{0,6})<\/span', str(text))[0]

            print(f'cost {result}')
            # return "".join(text).replace('£', '')
            return result
        except Exception as ex:
            print(ex)
            return 'Not found'

    def get_html_card_food(self) -> list["html"]:
        try:
            text = [etree.tostring(i) for i in self.html.xpath(
                '//li')]
            return text
        except:
            return ['Not found']

    def __call__(self, *args, **kwargs):
        date = datetime.now().strftime("%d.%m.%Y")
        url = self.url
        post_code = self.post_code
        city = self.city
        brand = self.brand
        address = self.address


        # parce block
        name_category = self.get_name_category()

        html_card_food = self.get_html_card_food()
        data = []
        for val in html_card_food:
            name = self.get_name_food(val)
            image_url = self.get_image_food(val)
            cost = self.get_cost_food(val)
            data.append({
                'Start date': date,
                'End date': date,
                'Brand':brand,
                'Address':address,
                'City':city,
                'Post_code':post_code,
                'Segment':'',
                'Category':name_category,
                'Category 2':'',
                'Category 3':'',
                'Category 4':'',
                'Item':name,
                'Source':'ubereats.com',
                'Region': 'UK',
                'Price(£)':cost,
                'Status':"on",
                'Picture':image_url,
                'Url_picture':image_url,
                'Url':url,

            })
        # print(data)
        return data

def scrolling_page(driver):
    for to_scrolling_element in driver.find_elements(By.XPATH, '(//main//ul)[1]/li'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)

def next_page(driver) ->list["Selenium element"]:
    #  $x('//main/div/div/a/')
    try:
        return driver.find_elements(By.XPATH, '//main/div/div/a/')
    except:
        return ["123"]

def parse(arg):
    url, post_code, city = arg
    print(f"PARSED {url}")

    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'

    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url=url)
    time.sleep(3)

    # $x('//main/div/div/a/')
    #
    #
    # $x('//main//ul')[1:]
    #
    # $x('(//main//ul)[2]/li[1]//span')
    # $x('(//main//ul)[2]/li[1]//img')
    # $x('//span[contains(text(), "£")]').map(i= > i.textContent) split('•')

    accept_click(driver)
    close_popup(driver)


    brand = get_brand(driver)
    address = get_address(driver, city)

    pages = next_page(driver)

    html_list_category_foods = []
    for page in pages:
        try:
            page.click()
            time.sleep(2)
        except:
            pass

        scrolling_page(driver)

        html_list_category_foods.append(get_html_category_list_foods(driver))

    html_list_category_foods = sum(html_list_category_foods, [])

    data = []
    for html_category in html_list_category_foods:
        menu = Parse_menu(
                            html_list_category_foods = html_category,
                            url = url,
                            post_code = post_code,
                            city = city,
                            brand = brand,
                            address = address,
                        )

        data.append(menu())

    data = sum(data, [])
    date = datetime.now().strftime("%d.%m.%Y")
    # pd.DataFrame(data).to_excel(f'uber_eats_{brand}_{post_code}_result_menu_price_{str(date)}.xlsx')
    data_frame = pd.DataFrame(data)
    DataBase().to_stg_table(data_frame=data_frame, name_stg_table='STG_UBER_EATS_PRICE')

def start_uber_eats_price():

    data = DataBase().get_table('uber_eats_list_url')
    urls_brands = []
    next(next(data)).apply(lambda x: urls_brands.append(tuple(x)), axis=1)

    with Pool(processes=6) as p:
        p.map(parse, urls_brands)


