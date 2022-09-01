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



def accept_click(driver):
    # $x('//button[contains(text(), "Accept")]')
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
        time.sleep(2)
    except:
        # '//button[contains(text(), "Ok")]'
        try:
            driver.find_element(By.XPATH, '//button[contains(text(), "Ok")]').click()
            time.sleep(2)
        except:
            print("Not found accept")
        pass

def get_address(driver, city):
    # address
    # $x('//*[contains(@class,"Menu")]//*[contains(@class,"Header")]//*[contains(text(),"Info")]')
    # $x('//span[contains(text(),"LS")]')
    # $x('(//div[contains(@id, "layout-list-map")]//div[contains(@class, "UIContentCard")]//div[contains(@class, "UILines")])[1]')
    try:
        driver.find_element(By.XPATH, '//*[contains(@class,"Menu")]//*[contains(@class,"Header")]//*[contains(text(),"Info")]').click()
        time.sleep(2)
        # address = driver.find_element(By.XPATH,
        #                     f'//span[contains(text(),"{city}")]').text
        address = driver.find_element(By.XPATH,
                            '(//div[contains(@id, "layout-list-map")]//div[contains(@class, "UIContentCard")]//div[contains(@class, "UILines")])[1]').text
    except:
        try:
            # '(//div[contains(@id, "layout-list-map")]//div[contains(@class, "UIContentCard")]//div[contains(@class, "UILines")])[1]'
            address = driver.find_element(By.XPATH,
                                          f'//*[contains(@id, "map")]//*[contains(text(), "{city}")]').text
        except:
            address = ''
    return address

def get_brand(driver):
    # brand = name place
    try:
        brand = driver.find_element(By.XPATH, '//h1').text
        return brand
    except:
        return "Npt found"

def get_html_category_list_foods(driver):
    #     $x('//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")]')
    return [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")]')]


def view_menu(driver):
    # $x('//span[contains(text(), "View menu")]')
    try:
        driver.find_element(By.XPATH, '//span[contains(text(), "View menu")]').click()
        time.sleep(2)
    except:
        pass

class Parse_menu():

    # menu
    #     $x('//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")]')
    #     category - $x('(//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")])[1]//h3')

    #     $x('(//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")])[1]//ul//div[contains(@data-testid, "image")]')
    #     $x('(//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")])[1]//ul/li[1]//p')
    #     $x('((//div[contains(@class,"MenuLayouts")]//div[contains(@id, "layout")])[1]//ul/li[1]//p)[1]')
    #     p[1] - name first()
    #     p[2] - description
    #     p[3] - kcal
    #     p[4] - cost last()

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
                '//h3')]
            return "".join(text)
        except:
            return 'Not found'

    def get_image_food(self, html):
        try:
            html = etree.HTML(html)
            url_image = [i.get('style') for i in html.xpath('//div[contains(@style, "background-image")]')]
            return url_image[0][23:-3]
        except:
            return 'Not found'

    def get_name_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath(
                '(//p)[1]')]
            return "".join(text)
        except:
            return 'Not found'


    def get_description_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath(
                '(//p)[2]')]
            return "".join(text)
        except:
            return 'Not found'

    def get_cost_food(self, html):
        try:
            html = etree.HTML(html)
            text = [i.text for i in html.xpath('//span[contains(text(), "£")]')]
            return "".join(text).replace('£', '')
        except:
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
                'Source':'deliveroo.co.uk',
                'Region': 'UK',
                'Price':cost,
                'Status':"on",
                'Picture':image_url,
                'Url_picture':image_url,
                'Url':url,

            })
        # print(data)
        return data

def scrolling_page(driver):
    for to_scrolling_element in driver.find_elements(By.XPATH, '//ul/li'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)


def save_image(data):
    for i in data:
        image = i
        name = name.strip()
        directory = 'kfc'
        try:
            reponse_img = requests.get(f"{image}")
            if reponse_img.status_code == 200:
                with open(f"{directory}/{name}.png", "wb") as file:
                    file.write(reponse_img.content)
        except:
            print(f"ERROR {name}")

def parse(arg):
    try:
        url, post_code, city = arg
        print(f"PARSED {url}")

        options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--lang=en-nz")
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")

        path = r'chromedriver.exe'

        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        driver.get(url=url)
        time.sleep(3)


        accept_click(driver)
        view_menu(driver)


        brand = get_brand(driver)
        address = get_address(driver, city)

        # print(1)
        driver.get(url=url)
        time.sleep(3)
        view_menu(driver)
        scrolling_page(driver)

        html_list_category_foods = get_html_category_list_foods(driver)
        # print(html_list_category_foods[0])
        data = []
        for html_category in html_list_category_foods:
            try:
                menu = Parse_menu(html_list_category_foods = html_category,
                                url = url,
                               post_code = post_code,
                               city = city,
                               brand = brand,
                               address = address,
                               )

                data.append(menu())
            except:
                continue
        data = sum(data, [])
        date = datetime.now().strftime("%d.%m.%Y")
        pd.DataFrame(data).to_excel(f'deliveroo_{brand}_{post_code}_result_menu_price_{str(date)}.xlsx')
    except:
        pass
if __name__ == '__main__':

    data = pd.read_excel('deliveroo_list_url.xlsx')
    with Pool(processes=1) as p:
        p.map(parse, zip(data['url'], data['post_code'], data['city']))