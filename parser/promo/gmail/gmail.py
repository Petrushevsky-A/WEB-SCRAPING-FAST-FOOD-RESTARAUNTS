import time
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import undetected_chromedriver.v2 as undetected_chrome
import pandas as pd

import numpy as np

from multiprocessing import Pool
from lxml import etree


def run_browser():
    # options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--start-maximized")
    # options.add_argument("--lang=en-nz")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # # options.add_argument(r"user-data-dir=C:\Users\qwerty\AppData\Local\Google\Chrome\User Data\Default")
    # path = r'chromedriver.exe'
    #
    url = 'https://www.google.com/gmail/about/'
    # path = r'chromedriver.exe'

    # driver = webdriver.Chrome(chrome_options=options, executable_path=


    driver = undetected_chrome.Chrome()
    driver.delete_all_cookies()
    time.sleep(2)
    # driver.get(url=url)
    driver.get(url)
    time.sleep(5)
    return driver

def authorization(driver):
    MAIL = 'fastfoodlondon2021@gmail.com'
    PASSWORD = 'Projectplaner123'
    # Войти
    try:
        driver.find_element(By.XPATH, '//a[contains(text(), "Sign")]').click()
        time.sleep(2)
    except:
        driver.find_element(By.XPATH, '//a[contains(text(), "Войти")]').click()
        time.sleep(2)

    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(MAIL)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(Keys.ENTER)
    time.sleep(2)

    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(PASSWORD)
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(Keys.ENTER)
    time.sleep(2)

    # sign in xpath
    # '//a[contains(text(), "Sign")]'
    # email xpath
    # '//input[@type="email"]'

    # password xpath
    # '//input[@type="password"]'

    # login and password
    # fastfoodlondon2021@gmail.com
    # Projectplaner123


    
def accept_click(driver):
    try:
        driver.find_element(By.XPATH, '//a[contains(text(), "OK")]').click()
    except:
        pass

def read_messeges(driver, list_messeges):

    # view messeges table in div class UI $x('//div[contains(@class, "UI")]')
    # $x('//div[@class="AO"]//table//tr')
    # next list
    # $x('//div[@role="toolbar"]/following-sibling::div//div[@aria-label="Older"]')
    data = []
    time.sleep(10)
    messeges = driver.find_elements(By.XPATH, '//div[@class="AO"]//table//tr')
    city = "London"
    post_code = "W1C 1LX"
    for messege in messeges:
        try:

            messege.click()
        except Exception as ex:
            print(ex)
            continue
        time.sleep(4)
        try:
            date = datetime.now().strftime("%d.%m.%Y")
        except:
            date = ['Not Found']
        try:
            # $x('//table[@role = "grid"]//span[@class="bog"]//span[@data-legacy-last-message-id]')
            head = driver.find_element(By.XPATH, '//table//h2').text
        except:
            head = ['Not Found']
        # $x('//table[@role="presentation"]//center//table//img')
        try:
            image = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//table[@role="presentation"]//table//img')]
        except:
            image = ['Not Found']
        try:
            text = [i.text for i in driver.find_elements(By.XPATH, '//table[@role="presentation"]//table//td')]
            text = [i.replace('\n', ' ').replace('\ufeff', '') for i in text]
        except:
            text = ['Not Found']
        try:
            hash_id = driver.current_url.split('/')[-1]
        except:
            hash_id = ['Not Found']
        try:
            print(date)
            print(head)
            print(image)
            print(hash_id)
            print(text)
        except:
            pass
        try:
            driver.back()
        except:
            try:
                driver.execute_script("window.history.go(-1)")
            except:
                to_all_mail(driver)
                index = messeges.index(messege)
                messeges = driver.find_elements(By.XPATH, '//div[@class="AO"]//table//tr')
                messeges = messeges[index:]
        time.sleep(2)
        data.append([date, post_code, city, head, image, text, hash_id])
    columns = {
        0: 'date',
        1: 'post_code',
        2: 'city',
        3: 'head',
        4: 'image',
        5: 'text',
        6: 'hash_id',
    }
    data = pd.DataFrame(data)
    data = data.rename(columns = columns)
    data.to_excel(f"gmail_messeges_{list_messeges}_{date}.xlsx")

def to_all_mail(driver):
    url = 'https://mail.google.com/mail/u/2/?ogbl#all'
    driver.get(url)
    time.sleep(3)

def to_next_page(driver):
    # $x('//div[@role="toolbar"]/following-sibling::div//div[@aria-label="Older"]/span')
    print(3)
    try:
        driver.find_element(By.XPATH, '//div[@role="toolbar"]/following-sibling::div//div[@aria-label="Older"]').click()
        time.sleep(2)
        print(4)
        return 1
    except:
        return -1
        print(5)
def parse():

    driver = run_browser()
    accept_click(driver)
    time.sleep(2)
    authorization(driver)
    time.sleep(2)
    to_all_mail(driver)
    time.sleep(2)
    number_list = 0

    while True:

        print(bool(driver.find_elements(By.XPATH, '//div[@role="toolbar"]/following-sibling::div//div[@aria-label="Older"][@aria-disabled="true"]')))

        number_list += 1
        print(1)
        read_messeges(driver, number_list)
        status = to_next_page(driver)
        print(2)
        if status== -1:
            break

        if not bool(driver.find_elements(By.XPATH, '//div[@role="toolbar"]/following-sibling::div//div[@aria-label="Older"][@aria-disabled="true"]')):
            break
    print('end')

    #
    # raise Exception



    # driver.close()
    # driver.quit()

    # data_all_offers = sum(data_all_offers, [])
    #
    # data = [pd.DataFrame([i]) for i in data_all_offers]
    #
    # data = pd.concat(data)
    # pd.DataFrame(data).to_excel(f'deliveroo_{post_code}.xlsx')


    columns = {
        0: 'dates',
        1: 'post_codes',
        2: 'city',
        3: 'head',
        4: 'names',
        5: 'descriptions',
        6: 'link_images',
        7: 'foods_category',
        8: 'delivery',
        9: 'times',
    }



if __name__ == '__main__':
    parse()

