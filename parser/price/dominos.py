import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


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
        print("Not found accept")
        pass


def get_city(driver):
    # $x('//span[@class="nav-store-name"]')
    try:
        city = driver.find_element(By.XPATH,
                            '//span[@class="nav-store-name"]').text
    except:
        city = ''
    return city



def get_html_category_list_foods(driver):
    # $x('//section[@class="category"]')
    return [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//section[@class="category"]')]


def get_category(driver):
    return [i.get_attribute('id') for i in driver.find_elements(By.XPATH, '//section[@class="category"]')]


class Parse_menu():

    # $x('(//main//ul)[2]/li[1]//span')
    # $x('(//main//ul)[2]/li[1]//img')
    # $x('//span[contains(text(), "£")]').map(i= > i.textContent) split('•')

    def __init__(self, html_list_category_foods,name_category, post_code , url, city, brand, address):
        self.html = etree.HTML(html_list_category_foods)
        self.name_category = name_category
        self.url = url
        self.post_code = post_code
        self.city = city
        self.brand = brand
        self.address = address

    def get_name_category(self):
        return self.name_category

    def get_image_food(self, html):
        # $x('(//section[@class="category"])[2]//img')
        try:
            html = etree.HTML(html)
            url_image = [i.get('src') for i in html.xpath('//img[contains(@class, "product-image")]')]
            return url_image[0]
        except:
            return 'Not found'

    def get_name_food(self, html):
        html = etree.HTML(html)
        try:
            text = [i.text for i in html.xpath(
                '//p[@class="h6"]')]
            text = "".join(text)
            if text == '':
                text = [i.text for i in html.xpath(
                    '//select[contains(@class, "product-variant")]/option[@selected="selected"]')]
                text = "".join(text[0])
            return text
        except:
            pass



    # def get_size_food(self, html):
    #     try:
    #         # '//span[contains(text(), "£")]'
    #         html = etree.HTML(html)
    #         text = [i.text for i in html.xpath('//*[contains(text(), "£")]')]
    #         return [i for i in text if '£' in i][0]
    #     except:
    #         return 'Not found'

    def get_cost_food(self, html):
        try:
            # '//span[contains(text(), "£")]'
            html = etree.HTML(html)
            text = [i.text for i in html.xpath('//*[contains(text(), "£")]')]
            return text[0].split()[-1].replace('£', '')
        except:
            return 'Not found'

    def get_html_card_food(self) -> list["html"]:
        # $x('(//section[@class="category"])[2]//article[contains(@class, "product")]')
        try:
            text = [etree.tostring(i) for i in self.html.xpath(
                '//article[contains(@class, "product")]')]
            return text
        except:
            return ['Not found']

    def get_size(self, html):
        try:
            # '//span[contains(text(), "£")]'
            html = etree.HTML(html)
            text = [i.text for i in html.xpath('//*[contains(text(), "£")]')]
            return text[0].split()[0] if not "£" in text[0].split()[0] else ''
        except:
            return 'Not found'

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
        for html_card in html_card_food:
            name = self.get_name_food(html_card)
            image_url = self.get_image_food(html_card)
            cost = self.get_cost_food(html_card)
            category_2 = self.get_size(html_card)
            data.append({
                'Start date': date,
                'End date': date,
                'Brand':brand,
                'Address':address,
                'City':city,
                'Post_code':post_code,
                'Segment':'',
                'Category':name_category,
                'Category 2':category_2,
                'Category 3':'',
                'Category 4':'',
                'Item': name,
                'Source': 'dominos.co.uk',
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
    # $x('//section[@class="category"]//article[contains(@class, "product")]')
    for to_scrolling_element in driver.find_elements(By.XPATH, '//section[@class="category"]//article[contains(@class, "product")]'):
        driver.execute_script("arguments[0].scrollIntoView();", to_scrolling_element)
        time.sleep(0.2)


def next_page(driver) ->list["Selenium element"]:
    #  $x('//main/div/div/a/')
    try:
        return driver.find_elements(By.XPATH, '//main/div/div/a/')
    except:
        return ["123"]


def input_post_code(driver, post_code):
    # $x('//input[@type="text"]')
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(post_code)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(Keys.ENTER)
    time.sleep(7)


def click_first_button_list(driver):
    # $x('//*[contains(text(), "Collect")]/ancestor::button')
    try:
        driver.find_element(By.XPATH, '//*[contains(text(), "Collect")]/ancestor::button').click()
        time.sleep(4)
    except:
        print("not found button collect")


def close_popup(driver):
    # $x('//button[contains(@class, "close")]')
    try:
        driver.find_element(By.XPATH, '//button[contains(@class, "close")]').click()
        time.sleep(2)
    except:
        print("not found button collect")


def get_address(driver):
    # $x('//span[@class="nav-store-name"]/ancestor::li')
    try:
        driver.find_element(By.XPATH,
                            '//span[@class="nav-store-name"]/ancestor::li').click()
        time.sleep(2)
    except:
        address = ''
    try:
        # $x('//*[contains(@data-ref-id, "address")]')
        address = ", ".join([i.text for i in driver.find_elements(By.XPATH,
                            '//*[contains(@data-ref-id, "address")]')])
    except:
        address = ''
    return address


def parse(post_code):

    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-nz")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    path = r'chromedriver.exe'
    url = 'https://www.dominos.co.uk/'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url=url)
    time.sleep(3)


    accept_click(driver)


    input_post_code(driver, post_code)
    click_first_button_list(driver)
    close_popup(driver)



    brand = "Dominos"

    scrolling_page(driver)
    html_list_category_foods = get_html_category_list_foods(driver)
    list_category = get_category(driver)

    city = get_city(driver)
    address = get_address(driver)


    data = []
    for html_category, name_category in zip(html_list_category_foods, list_category):

        menu = Parse_menu(
                            html_list_category_foods = html_category,
                            name_category =  name_category,
                            url = url,
                            post_code = post_code,
                            city = city,
                            brand = brand,
                            address = address,
                       )

        data.append(menu())

    data = sum(data, [])
    # print(data)

    date = datetime.now().strftime("%d.%m.%Y")
    pd_data = pd.DataFrame(data)
    pd_data.to_excel(f'dominos_price_{post_code}_result_menu_price_{str(date)}.xlsx')

    # for pd_i in pd_data.iterrows():
    #
    #     src_img = pd_i['Picture']
    #
    #     print(src_img)
    #     directory = "dominos_img"
    #     name_img = pd_i['Item'].strip()
    #     try:
    #         reponse_img = requests.get(f"{src_img}")
    #         if reponse_img.status_code == 200:
    #             with open(f"{directory}/{name_img}.jpg", "wb") as file:
    #                 file.write(reponse_img.content)
    #     except:
    #         print(f"ERROR {src_img}")


if __name__ == '__main__':
    post_codes = [
        'W1C 1LX',
        'CF10 1PN',
        # 'BT1 5AA',
        # 'G1 3SQ',
        # 'B2 4QA',
        # 'L1 8JQ',
        # 'LS1 1UR',
        # 'M2 5DB',
    ]

    with Pool(processes=4) as p:
        p.map(parse, post_codes)



