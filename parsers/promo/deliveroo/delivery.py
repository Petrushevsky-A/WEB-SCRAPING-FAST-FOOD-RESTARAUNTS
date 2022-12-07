import time
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
import numpy as np

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'



post_codes = [
        'W1C 1LX',
        'CF10 1PN',
        'BT1 5AA',
        'G1 3SQ',
        'B2 4QA',
        'L1 8JQ',
        'LS1 1UR',
        'M2 5DB',
        ]

url = 'https://deliveroo.co.uk/'

    #  $x('//li[contains(@class, "HomeFeedGrid")][3]/div[contains(@class, "HomeFeed")]/div/div//ul/li[contains(@class, "Slide")]')

for post_code in post_codes[2:]:
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
    time.sleep(1)

    # set input
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(f'{post_code}')
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(Keys.ENTER)
    time.sleep(8)

    driver.find_element(By.XPATH, '//button/span[text() = "OK"]').click()
    time.sleep(2)
    # нужно отлистать весь лист чтобы подгрузились все данные
    # нажимает еще пока не подгрузяться все таблички
    # '//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]'
    # для прогрузки информации необходимо прокрутить сайд бар
    data = []
    card_deals = driver.find_elements(By.XPATH, '//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li')
    for id_card, card_deal in enumerate(card_deals, 1):
        def get_info_card(driver, id):
            head = driver.find_element(By.XPATH, '//h3[contains(text(),  "Up to")]').get_attribute('innerHTML')
            head = head.split('<span')[0]
            print(head)

            names = driver.find_element(By.XPATH, f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]/div/div/a/span/span[2]/div[2]/ul/li[1]').text
            print(names)

            descriptions = driver.find_element(By.XPATH, f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]//div[contains(@class, "PromotionTagOverlay")]').text


            print(descriptions)

            foods_category = driver.find_element(By.XPATH, f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]/div/div/a/span/span[2]/div[2]/ul/li[2]').text


            print(foods_category)

            link_images = driver.find_element(By.XPATH, f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]//div[contains(@style, "background-image: url")]').get_attribute('style')[23:-3]



            delivery = driver.find_element(By.XPATH,
                                                             f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]/div/div/a/span/span[2]/div[2]/ul/li[3]').text


            print(delivery)
            times = driver.find_element(By.XPATH, f'//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]/li[{id}]/div/div/a/span/span[2]/div[1]/ul').text

            print(times)
            date = datetime.now().strftime("%d.%m.%Y")
            city = driver.current_url.split('/')[4]
            return [date,post_code, city, head, names, descriptions, link_images, foods_category, delivery, times]
        if card_deal.is_displayed():
            data.append(get_info_card(driver, id_card))

        else:
            button = driver.find_element(By.XPATH,
                                         '//h3[contains(text(),  "Up to")]/ancestor::li//button[@aria-label="Next"]')
            if not button.is_displayed():
                break
            else:
                button.click()
            time.sleep(3)

            data.append(get_info_card(driver, id_card))


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
    print(data)
    data = pd.DataFrame(data)

    data = data.rename(columns=columns)

    data.to_excel(f'delivery_50cent_{post_code}.xlsx')
    driver.close()
    driver.quit()



